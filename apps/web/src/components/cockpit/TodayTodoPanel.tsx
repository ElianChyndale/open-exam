'use client';

import { useCallback, useEffect, useState } from 'react';
import { CheckCircle2, Circle, ClipboardPlus, Plus, Trash2 } from 'lucide-react';

import { TodoState, TodoTask, todosApi } from '@/lib/api';
import { queueTodoWrite } from '@/lib/offline';

export function TodayTodoPanel({ studyPlan }: { studyPlan: Record<string, unknown> | null }) {
  const [todo, setTodo] = useState<TodoState | null>(null);
  const [text, setText] = useState('');
  const [deadline, setDeadline] = useState('');
  const [error, setError] = useState('');
  const [progressDrafts, setProgressDrafts] = useState<Record<string, number>>({});

  const refresh = useCallback(async () => {
    try {
      setTodo(await todosApi.getToday());
      setProgressDrafts({});
      setError('');
    } catch {
      setError('Todo 加载失败，请确认本地 API 已启动。');
    }
  }, []);

  useEffect(() => {
    void refresh();
  }, [refresh]);

  const optimistic = async (
    next: TodoState,
    operation: () => Promise<TodoState>,
    retry: { path: string; method: string; body?: Record<string, unknown> },
  ) => {
    const previous = todo;
    setTodo(next);
    setError('');
    try {
      setTodo(await operation());
    } catch (reason) {
      setTodo(previous);
      setError(reason instanceof Error && reason.message.includes('409')
        ? 'Todo 已在其他位置更新，已刷新最新版本。'
        : 'Todo 更新失败，已回滚并加入离线重试队列。');
      if (!(reason instanceof Error && reason.message.includes('409'))) {
        await queueTodoWrite(retry.path, retry.method, retry.body);
      }
      await refresh();
    }
  };

  const addTask = async () => {
    if (!todo || !text.trim()) return;
    try {
      setTodo(await todosApi.create({
        text: text.trim(),
        deadline,
        expected_revision: todo.revision,
        date: todo.date,
      }));
      setText('');
      setDeadline('');
      setError('');
    } catch {
      await queueTodoWrite('/api/todos/tasks', 'POST', {
        text: text.trim(), deadline, expected_revision: todo.revision, date: todo.date,
      });
      setError('新增任务失败，已加入离线重试队列。');
      await refresh();
    }
  };

  const toggle = (task: TodoTask) => {
    if (!todo) return;
    const completed = task.status !== 'completed';
    const next = {
      ...todo,
      revision: todo.revision + 1,
      tasks: todo.tasks.map((item) => item.task_id === task.task_id
        ? { ...item, status: completed ? 'completed' as const : 'pending' as const, progress: completed ? 100 : 0 }
        : item),
    };
    void optimistic(next, () => todosApi.toggle(task.task_id, todo.revision), {
      path: `/api/todos/tasks/${task.task_id}/toggle`,
      method: 'POST',
      body: { expected_revision: todo.revision },
    });
  };

  const remove = (task: TodoTask) => {
    if (!todo) return;
    const next = {
      ...todo,
      revision: todo.revision + 1,
      tasks: todo.tasks.filter((item) => item.task_id !== task.task_id),
    };
    void optimistic(next, () => todosApi.remove(task.task_id, todo.revision), {
      path: `/api/todos/tasks/${task.task_id}?expected_revision=${todo.revision}`,
      method: 'DELETE',
    });
  };

  const updateProgress = (task: TodoTask, progress: number) => {
    if (!todo) return;
    const next = {
      ...todo,
      revision: todo.revision + 1,
      tasks: todo.tasks.map((item) => item.task_id === task.task_id ? { ...item, progress } : item),
    };
    void optimistic(next, () => todosApi.update(task.task_id, { progress, expected_revision: todo.revision }), {
      path: `/api/todos/tasks/${task.task_id}`,
      method: 'PATCH',
      body: { progress, expected_revision: todo.revision },
    });
  };

  const setProgressDraft = (taskId: string, progress: number) => {
    setProgressDrafts((current) => ({ ...current, [taskId]: progress }));
  };

  const commitProgressDraft = (task: TodoTask) => {
    const draft = progressDrafts[task.task_id];
    if (draft === undefined || draft === task.progress) return;
    setProgressDrafts((current) => {
      const next = { ...current };
      delete next[task.task_id];
      return next;
    });
    updateProgress(task, draft);
  };

  const importPlan = async () => {
    if (!studyPlan || !window.confirm('确认将今日学习计划导入 Todo？重复任务会自动跳过。')) return;
    try {
      setTodo(await todosApi.importStudyPlan(studyPlan, true));
      setError('');
    } catch {
      await queueTodoWrite('/api/todos/import-study-plan', 'POST', { plan: studyPlan, confirmed: true });
      setError('学习计划导入失败，已加入离线重试队列。');
      await refresh();
    }
  };

  return (
    <section className="card space-y-4" aria-labelledby="today-todo-title">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h3 id="today-todo-title" className="text-sm font-semibold">今日 Todo</h3>
          <p className="text-xs text-muted">事件重放驱动，Daily Review 固定于 20:00。</p>
        </div>
        <button type="button" onClick={importPlan} className="flex items-center gap-2 text-xs text-accent">
          <ClipboardPlus size={15} /> 导入今日学习计划
        </button>
      </div>

      <div className="grid gap-2 sm:grid-cols-[1fr_110px_auto]">
        <input value={text} onChange={(event) => setText(event.target.value)} placeholder="新增任务" className="input" />
        <input value={deadline} onChange={(event) => setDeadline(event.target.value)} type="time" aria-label="任务截止时间" className="input" />
        <button type="button" onClick={addTask} className="btn-primary flex items-center justify-center gap-1">
          <Plus size={15} /> 新增
        </button>
      </div>

      {error && <p role="status" className="text-xs text-danger">{error}</p>}

      <ul className="space-y-3">
        {todo?.tasks.map((task) => (
          <li key={task.task_id} className="flex items-center gap-3 rounded-lg border border-line p-3">
            <button type="button" onClick={() => toggle(task)} aria-label={`切换 ${task.text} 完成状态`} className="text-accent">
              {task.status === 'completed' ? <CheckCircle2 size={18} /> : <Circle size={18} />}
            </button>
            <div className="min-w-0 flex-1">
              <div className={`text-sm ${task.status === 'completed' ? 'line-through text-muted' : ''}`}>{task.text}</div>
              <div className="mt-1 flex items-center gap-2">
                <input
                  type="range"
                  min="0"
                  max="100"
                  step="10"
                  value={progressDrafts[task.task_id] ?? task.progress}
                  aria-label={`${task.text} 进度`}
                  onChange={(event) => setProgressDraft(task.task_id, Number(event.target.value))}
                  onMouseUp={() => commitProgressDraft(task)}
                  onTouchEnd={() => commitProgressDraft(task)}
                  onKeyUp={() => commitProgressDraft(task)}
                  className="w-28"
                />
                <span className="text-xs text-muted">{progressDrafts[task.task_id] ?? task.progress}%{task.deadline ? ` · ${task.deadline}` : ''}</span>
              </div>
            </div>
            {task.source !== 'system' && (
              <button type="button" onClick={() => remove(task)} aria-label={`删除 ${task.text}`} className="text-muted hover:text-danger">
                <Trash2 size={16} />
              </button>
            )}
          </li>
        ))}
      </ul>
    </section>
  );
}
