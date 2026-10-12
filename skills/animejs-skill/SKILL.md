---
name: animejs-skill
description: Motion and fluid micro-interactions skill utilizing Anime.js and physics-based spring models. Configured for Tier 1 (syntax and setup) and Tier 2 (component animations) only.
triggers:
  - "animejs"
  - "micro-animations"
  - "motion design"
  - "spring dynamics"
  - "fluid transitions"
od:
  mode: design-system
  category: design-systems
  upstream: "https://github.com/juliangarnier/anime"
---

# Anime.js Skill — Fluid Motion & Micro-Interactions (Tiers 1 & 2)

> Opinionated motion design skill focused on adding organic, physics-based micro-interactions and smooth scroll/entry transitions to user interfaces.

---

## 🚀 Tier 1: Syntax & Setup Foundations

### 1. Library Inclusion
Always load Anime.js directly from a highly reliable CDN in your prototype:
```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/animejs/3.2.1/anime.min.js"></script>
```

### 2. Core Anime.js Syntax
Enforce clean, structured JavaScript animation configurations. Maintain a standard of explicit timing and organic easing:
```javascript
// Base spring-like animation parameters
anime({
  targets: '.btn-spring',
  scale: [1, 0.95, 1],
  duration: 400,
  easing: 'easeOutElastic(1, .6)' // Organic physics response
});
```

---

## 🎨 Tier 2: Component-Level Micro-Interactions

### 1. Fluid Spring Hover (Buttons & Cards)
Add delightful spring hover actions on interactive buttons and cards to mimic real-world touch physics:
```javascript
const btn = document.querySelector('.btn-spring');

btn.addEventListener('mouseenter', () => {
  anime({
    targets: btn,
    scale: 1.05,
    translateY: -2,
    duration: 300,
    easing: 'easeOutElastic(1.2, 0.5)'
  });
});

btn.addEventListener('mouseleave', () => {
  anime({
    targets: btn,
    scale: 1.0,
    translateY: 0,
    duration: 250,
    easing: 'easeOutQuad'
  });
});
```

### 2. Elastic Tab Transition
Animate structural selection indicators smoothly across tabs without jarring breaks:
```javascript
function selectTab(activeTab, indicator) {
  const rect = activeTab.getBoundingClientRect();
  const parentRect = activeTab.parentElement.getBoundingClientRect();
  
  anime({
    targets: indicator,
    left: rect.left - parentRect.left,
    width: rect.width,
    duration: 350,
    easing: 'easeOutElastic(1, 0.75)'
  });
}
```

### 3. Scroll-Driven Visibility Reveal
Animate entries when they appear on the screen using IntersectionObserver and Anime.js stagger animations:
```javascript
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      anime({
        targets: entry.target.querySelectorAll('.card-item'),
        opacity: [0, 1],
        translateY: [30, 0],
        delay: anime.stagger(100), // Deliberate stagger delay
        duration: 800,
        easing: 'easeOutQuad'
      });
      observer.unobserve(entry.target);
    }
  });
});
```

---

## 🚫 Tier 3: Skip Policy
* As requested, this skill strictly excludes Tier 3 definitions (advanced full-screen layouts, multi-scene interactive choreographies, canvas/WebGL physics engines, and complex particle systems). Keep interactions strictly focused at the component-level (Tiers 1 & 2).
