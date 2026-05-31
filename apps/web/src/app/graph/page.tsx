'use client';

import { useEffect, useState } from 'react';
import { Background, Controls, MiniMap, ReactFlow, useEdgesState, useNodesState, type Edge, type Node } from '@xyflow/react';
import { GitBranch, Plus, Save } from 'lucide-react';
import { graphApi, GraphRecord } from '@/lib/api';
import { Badge, Button, Field, Surface } from '@/components/ui/ui';

type GraphNodeData = { label: string; sourceKind: GraphRecord['source_kind']; notes?: string };

export default function GraphPage() {
  const [nodes, setNodes, onNodesChange] = useNodesState<Node<GraphNodeData>>([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState<Edge>([]);
  const [label, setLabel] = useState('');
  const [saved, setSaved] = useState(false);

  const refresh = () => graphApi.get().then((graph) => {
    setNodes(graph.nodes.map((node) => ({
      id: node.id,
      position: { x: node.x ?? 0, y: node.y ?? 0 },
      data: { label: node.label, sourceKind: node.source_kind, notes: node.notes },
      draggable: !node.locked,
      className: node.source_kind === 'personal' ? 'graph-node-personal' : 'graph-node-locked',
    })));
    setEdges(graph.edges.map((edge) => ({ id: edge.id, source: edge.source ?? '', target: edge.target ?? '', label: edge.label })));
  });

  useEffect(() => { refresh(); }, []);

  const addPersonalNode = () => {
    if (!label.trim()) return;
    setNodes((current) => [...current, {
      id: `personal-${Date.now()}`,
      position: { x: 120, y: 120 },
      data: { label, sourceKind: 'personal' },
      draggable: true,
      className: 'graph-node-personal',
    }]);
    setLabel('');
    setSaved(false);
  };

  const save = async () => {
    const personalNodes: GraphRecord[] = nodes.filter((node) => node.data.sourceKind === 'personal').map((node) => ({
      id: node.id,
      label: node.data.label,
      source_kind: 'personal',
      node_type: 'note',
      x: node.position.x,
      y: node.position.y,
      notes: node.data.notes,
    }));
    await graphApi.updateOverlay(personalNodes, []);
    setSaved(true);
  };

  return (
    <div className="mx-auto max-w-7xl space-y-4">
      <header className="flex flex-wrap items-end justify-between gap-3">
        <div>
          <p className="metric-label">Official spine + personal overlay</p>
          <h1 className="mt-1 text-3xl font-semibold tracking-tight">Knowledge graph</h1>
          <p className="mt-2 text-sm text-muted">Official and evidence nodes stay locked. Personal study notes remain movable and editable.</p>
        </div>
        <div className="flex gap-2"><Badge tone="accent">{nodes.length} nodes</Badge><Badge>Overlay editable</Badge></div>
      </header>
      <Surface className="flex flex-wrap gap-2">
        <Field className="max-w-sm" value={label} onChange={(event) => setLabel(event.target.value)} placeholder="Add a personal study node" />
        <Button variant="secondary" onClick={addPersonalNode}><Plus size={15} /> Add note</Button>
        <Button onClick={save}><Save size={15} /> Save overlay</Button>
        {saved ? <span className="self-center text-xs text-success">Personal overlay saved.</span> : null}
      </Surface>
      <Surface className="h-[68vh] overflow-hidden p-0">
        <ReactFlow nodes={nodes} edges={edges} onNodesChange={onNodesChange} onEdgesChange={onEdgesChange} fitView>
          <Background /><MiniMap pannable zoomable /><Controls />
        </ReactFlow>
      </Surface>
    </div>
  );
}
