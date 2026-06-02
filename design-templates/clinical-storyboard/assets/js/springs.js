/*
 * clinical-storyboard — spring physics micro-interactions.
 * Co-Authored-By: aba-bcba-expert <sheveenbrown@gmail.com>
 *
 * Programmed to support Anime.js v4 named tree-shakeable functions and browser CDN overrides.
 */

// Safe runtime detection for Node servers, browser bundles, and browser window script engines
const getAnimate = () => {
  if (typeof window !== 'undefined' && window.anime) {
    return (targets, params) => window.anime({ targets, ...params });
  }
  try {
    const animeModule = require('animejs');
    return animeModule.animate || animeModule.default || animeModule;
  } catch (e) {
    // Graceful fallback for offline static files or test specs
    return (targets, params) => {
      const elements = typeof targets === 'string' ? document.querySelectorAll(targets) : [targets];
      elements.forEach(el => {
        if (el && el.style) {
          Object.keys(params).forEach(key => {
            if (key !== 'duration' && key !== 'easing' && key !== 'delay') {
              el.style[key] = params[key];
            }
          });
        }
      });
    };
  }
};

const animate = getAnimate();

/**
 * Attaches elastic scaling spring transitions on cursor hovers (Fitts' Law target)
 * @param {HTMLElement | string} targets Selector or element reference
 */
export function wireElasticHover(targets) {
  if (typeof window === 'undefined') return;
  const elements = typeof targets === 'string' ? document.querySelectorAll(targets) : [targets];
  
  elements.forEach(el => {
    if (!el) return;
    el.addEventListener('mouseenter', () => {
      animate(el, {
        scale: 1.018,
        translateY: -3,
        duration: 350,
        easing: 'easeOutElastic(1.2, 0.62)'
      });
    });
    
    el.addEventListener('mouseleave', () => {
      animate(el, {
        scale: 1.0,
        translateY: 0,
        duration: 250,
        easing: 'easeOutQuad'
      });
    });
  });
}

/**
 * Standard staggered reveal animation for storyboard grids and pages on layout load
 * @param {string} selector Class or ID matching revealable elements
 */
export function triggerStaggeredReveal(selector) {
  if (typeof window === 'undefined') return;
  const targets = document.querySelectorAll(selector);
  if (targets.length === 0) return;

  animate(targets, {
    opacity: [0, 1],
    translateY: [16, 0],
    delay: (el, i) => i * 60,
    duration: 650,
    easing: 'easeOutQuad'
  });
}
