---
name: frontend-performance-profiler
description: Reviews frontend runtime performance for unnecessary client components, excessive hydration, huge bundles, duplicate dependencies, bad image loading, slow fonts, layout shift, expensive React renders, bad suspense or loading states, excessive client-side fetching, blocking third-party scripts, and bad mobile performance. Use when reviewing UX/runtime performance or Core Web Vitals risk.
---

# Frontend Performance Profiler

Review frontend performance as a user-experience and runtime problem.

## Core checks

- Unnecessary client components
- Excessive hydration and client boundaries
- Huge bundles and duplicate dependencies
- Bad image loading and missing dimensions
- Slow fonts and font blocking
- Layout shift and unstable layouts
- Expensive React renders
- Weak suspense and loading states
- Excessive client-side fetching
- Blocking third-party scripts
- Mobile performance regressions

## Core Web Vitals

Target LCP, INP, and CLS explicitly. Flag work that hurts page load, interactivity, or layout stability.

## Output

Return the highest-cost paths first, then a short list of changes that reduce load, interaction delay, or layout shift.
