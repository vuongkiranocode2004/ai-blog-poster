# Frontend Guideline Document

This document lays out how we’ll build and maintain the web interface (dashboard) for the Blog Post Creator API. It covers our overall structure, design values, styling rules, component setup, state handling, routing, performance tips, testing, and more. Anyone—whether you’re a designer, developer, or stakeholder—should find it clear and actionable.

## 1. Frontend Architecture

We’re using **React** (with **TypeScript**) as our base framework. Around it, we have:

• **Vite** for fast builds and hot reloading.  
• **Tailwind CSS** for utility-based styling.  
• **React Router** to manage pages and URLs.  
• **Context API** (plus React Query) to share data and cache API calls.  

How this helps:

• **Scalability:** Vite + React supports modular code splitting. As we grow, we can add sections without slowing down builds.  
• **Maintainability:** Component-based React and Tailwind utilities keep styles and logic in small, reusable pieces.  
• **Performance:** Vite’s fast dev server, React.lazy, and React Query’s caching make the app load quickly and update smoothly.

## 2. Design Principles

We follow three core rules:

1. Usability: Keep every screen clear—labels on forms, simple instructions, consistent buttons.  
2. Accessibility: Use semantic HTML (headings, forms, buttons) plus ARIA roles and focus states so screen readers and keyboard users can navigate.  
3. Responsiveness: The dashboard works on desktop, tablet, and mobile by using flexible layouts (CSS Grid/Flexbox) and Tailwind’s responsive helpers.

How it shows up:

• Inputs have proper `label` tags and error messages announce themselves.  
• Colors meet WCAG contrast standards.  
• Layout stacks vertically on small screens and splits into panels on larger ones.

## 3. Styling and Theming

### CSS Methodology

We rely on **Tailwind CSS** (no global CSS files) to keep styles co-located with components. We group related utilities (padding, margin, color) rather than writing handcrafted CSS.

### Theming

We support light and dark modes using a top-level CSS class (`.light` / `.dark`). Tailwind’s `dark:` variants automatically switch colors. Future themes can be added by extending the Tailwind config.

### Visual Style

• Overall look: **Modern flat design** with subtle shadows.  
• Key effect: light glass-like panels (frosted backgrounds) for modals and cards.  

### Color Palette

Primary:  
  - Blue 500 (#3B82F6)  
  - Blue 600 (#2563EB)  
Secondary:  
  - Emerald 500 (#10B981)  
Accent:  
  - Amber 400 (#FBBF24)  
Neutral:  
  - Gray 100 (#F3F4F6)  
  - Gray 700 (#374151)  
  - White (#FFFFFF)  
  - Black (#000000)  
Error:  
  - Red 500 (#EF4444)

### Typography

Font family: **Inter** (sans-serif) for a clean, modern feel.  
Headings: bold weights (600–700).  
Body text: regular (400).  
Line height: 1.5 for readability.

## 4. Component Structure

We organize code by **feature folders** under `src/components/`, for example:

```text
src/
 └ components/
     ├ GenerateForm/
     │   ├ GenerateForm.tsx
     │   └ generateForm.css (Tailwind config imports)
     ├ ResultsList/
     └ Shared/Button.tsx
```

Each folder holds its main component, local styles (if any), and tests. Shared UI parts like buttons, inputs, or modals live under `components/Shared`.

Why this matters:

• You quickly find all code for a feature in one place.  
• Reusable components reduce duplication.  
• Small, focused files are easier to read and test.

## 5. State Management

### Local State

Use React’s `useState` or `useReducer` for component-specific state (form fields, open/close modals).

### Global State & Data Fetching

We use **React Query** for API calls (`/generate/blog`, `/generate/image`, `/metadata/config`). It handles caching, loading states, and retries.  

For truly global UI flags (e.g., theme mode), we use React’s Context API with a small provider at `src/context/`.

How it flows:

1. User opens the form page.  
2. React Query fetches metadata config once and caches it.  
3. Form fields update local state until submission.  
4. Submit triggers a React Query mutation, showing a spinner until completion.  
5. On success, results are stored in React Query’s cache and displayed in the ResultsList component.

## 6. Routing and Navigation

We leverage **React Router v6**:

Routes:
 • `/` → Dashboard home (quick links + stats)  
 • `/generate` → Blog/Image generation form  
 • `/results/:taskId` → View generated files  
 • `/settings` → User preferences (theme, internal link style)  

Navigation:

A top nav bar with links to each section. Active link is highlighted. On mobile, a hamburger menu toggles a side drawer.

## 7. Performance Optimization

Key strategies:

• **Code Splitting:** Use `React.lazy` and `Suspense` for heavy pages (e.g., Results view).  
• **Optimized Assets:** Only load SVG icons as React components; compress PNG/JPEGs for illustrations.  
• **Bundle Analysis:** Regularly run `npm run analyze` to check bundle sizes.  
• **Prefetching:** Preload metadata config on app start so `/generate` loads instantly.  

These steps keep initial load under 2 seconds on typical connections.

## 8. Testing and Quality Assurance

### Unit Tests

• **Jest** + **React Testing Library** for components: simulate user input, verify UI changes and API calls are mocked.

### Integration Tests

• Combine components and context providers in tests to ensure form → submission → results flow works without mocking internal logic.

### End-to-End Tests

• **Cypress** for key user journeys: fill out generation form, view results, switch themes, handle errors.

### Linting & Formatting

• **ESLint** (with React and TypeScript rules) and **Prettier** to keep code style uniform.  
• **Commit hooks** (via Husky) run lint and tests before every push.

## 9. Conclusion and Overall Frontend Summary

We’ve outlined a straightforward, modern, and accessible React-based frontend:

• **Architecture:** Vite + React + Tailwind + React Query for speed and modularity.  
• **Design:** Flat, glass-like panels, strong contrast, mobile-first responsiveness.  
• **Components:** Feature-based organization for clarity and reuse.  
• **State & Data:** React Query handles API logic; Context API covers UI flags.  
• **Routing:** Simple, predictable URL structure with React Router.  
• **Performance:** Lazy loading, asset optimization, bundle analysis.  
• **Quality:** Unit, integration, and E2E testing, plus linting and formatting.

Together, these guidelines ensure our front end is easy to develop, easy to maintain, and provides a smooth experience for developers and SEO specialists who use our Blog Post Creator API.