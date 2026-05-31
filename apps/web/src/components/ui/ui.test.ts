import { createElement } from 'react';
import { render, screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';
import { Button, Surface } from './ui';

describe('Apple workspace primitives', () => {
  it('renders a labeled surface and primary action', () => {
    render(
      createElement(
        Surface,
        { 'aria-label': 'Daily workspace' },
        createElement(Button, null, 'Start review'),
      ),
    );

    expect(screen.getByLabelText('Daily workspace')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Start review' })).toHaveClass('button-primary');
  });
});
