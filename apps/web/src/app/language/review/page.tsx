'use client';

import { useEffect, useState } from 'react';

import { languageApi, LanguageCard, LanguageItem } from '@/lib/api';
import { LanguageShell } from '@/components/language/LanguageShell';
import { FlipReviewCard } from '@/components/motion/FlipReviewCard';

const ratings = ['again', 'hard', 'good', 'easy'] as const;

export default function LanguageReview() {
  const [cards, setCards] = useState<LanguageCard[]>([]);
  const [items, setItems] = useState<LanguageItem[]>([]);
  const [message, setMessage] = useState('');
  const refresh = () => Promise.all([languageApi.dueCards(), languageApi.items()]).then(([cardData, itemData]) => { setCards(cardData.cards); setItems(itemData.items); });
  useEffect(() => { void refresh(); }, []);
  const card = cards[0];

  const generate = async () => {
    if (!items[0]) return setMessage('Collect an item in Corpus first.');
    await languageApi.generateCards(items[0].item_id);
    await refresh();
  };
  const rate = async (rating: typeof ratings[number]) => {
    if (!card) return;
    const reviewed = await languageApi.reviewCard(card.card_id, rating);
    setMessage(`Next review: ${new Date(reviewed.due_at).toLocaleString()}`);
    await refresh();
  };

  return (
    <LanguageShell title="Recall the expression before the answer appears." eyebrow="Contextual review">
      <section className="motion-reveal mx-auto max-w-2xl space-y-4">
        {card ? <FlipReviewCard front={card.front_payload.prompt} back={<><span>{card.back_payload.answer}</span><p className="mt-4 text-sm font-normal text-muted">{card.context_window.join(' · ')}</p></>} /> : <div className="card text-sm text-muted">No due cards. Generate a small contextual deck from your first collected item.</div>}
        <div className="grid grid-cols-4 gap-2">{ratings.map((rating) => <button key={rating} type="button" disabled={!card} onClick={() => rate(rating)} className="rounded-lg border border-line bg-surface-raised px-2 py-2 text-xs capitalize text-muted hover:text-accent disabled:opacity-40">{rating}</button>)}</div>
        <button type="button" onClick={generate} className="text-sm text-accent">Generate cards from first corpus item</button>
        {message ? <p role="status" className="text-sm text-muted">{message}</p> : null}
      </section>
    </LanguageShell>
  );
}
