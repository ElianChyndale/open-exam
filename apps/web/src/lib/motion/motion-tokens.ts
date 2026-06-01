export const motionTokens = {
  duration: { micro: 0.12, fast: 0.22, normal: 0.38, slow: 0.65 },
  ease: { standard: 'power2.out', enter: 'power3.out', exit: 'power2.in', emphasized: 'expo.out' },
  stagger: { list: 0.035, cards: 0.06, graph: 0.015 },
} as const;
