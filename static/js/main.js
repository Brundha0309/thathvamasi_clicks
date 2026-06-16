/* ═══════════════════════════════════════════
   THATHVAMASI CLICKS — main.js
   ═══════════════════════════════════════════ */

// ── NAVBAR SCROLL ──────────────────────────
const navbar = document.getElementById('navbar');
window.addEventListener('scroll', () => {
  navbar && navbar.classList.toggle('scrolled', window.scrollY > 60);
});

// ── HAMBURGER ──────────────────────────────
const hamburger = document.getElementById('hamburger');
const navLinks  = document.getElementById('navLinks');
hamburger && hamburger.addEventListener('click', () => {
  navLinks.classList.toggle('open');
  const spans = hamburger.querySelectorAll('span');
  if(navLinks.classList.contains('open')){
    spans[0].style.transform='rotate(45deg) translate(5px,5px)';
    spans[1].style.opacity='0';
    spans[2].style.transform='rotate(-45deg) translate(5px,-5px)';
  } else {
    spans.forEach(s=>{ s.style.transform=''; s.style.opacity=''; });
  }
});

// Close menu on link click
navLinks && navLinks.querySelectorAll('a').forEach(a => {
  a.addEventListener('click', () => {
    navLinks.classList.remove('open');
    hamburger && hamburger.querySelectorAll('span').forEach(s=>{ s.style.transform=''; s.style.opacity=''; });
  });
});

// ── SCROLL REVEAL ──────────────────────────
const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if(e.isIntersecting){ e.target.classList.add('visible'); }
  });
}, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

document.querySelectorAll('.reveal').forEach(el => revealObserver.observe(el));

// ── TOAST ──────────────────────────────────
function showToast(msg, type='success') {
  const toast = document.getElementById('toast');
  if(!toast) return;
  toast.textContent = msg;
  toast.className = `toast ${type}`;
  toast.classList.add('show');
  setTimeout(() => toast.classList.remove('show'), 4000);
}

// ── LIGHTBOX ───────────────────────────────
let lbImages = [];
let lbIndex  = 0;

function openLightbox(src, caption) {
  const lb = document.getElementById('lightbox');
  const img = document.getElementById('lbImg');
  if(!lb || !img) return;
  // collect all portfolio images on page
  lbImages = Array.from(document.querySelectorAll('.portfolio-item img, .service-card img')).map(i=>i.src);
  lbIndex = lbImages.indexOf(src);
  if(lbIndex < 0){ lbImages = [src]; lbIndex = 0; }
  img.src = lbImages[lbIndex];
  lb.classList.add('open');
  document.body.style.overflow = 'hidden';
}

document.getElementById('lbClose') && document.getElementById('lbClose').addEventListener('click', closeLightbox);
document.getElementById('lightbox') && document.getElementById('lightbox').addEventListener('click', (e) => {
  if(e.target.id==='lightbox') closeLightbox();
});
document.getElementById('lbPrev') && document.getElementById('lbPrev').addEventListener('click', (e) => {
  e.stopPropagation();
  lbIndex = (lbIndex - 1 + lbImages.length) % lbImages.length;
  document.getElementById('lbImg').src = lbImages[lbIndex];
});
document.getElementById('lbNext') && document.getElementById('lbNext').addEventListener('click', (e) => {
  e.stopPropagation();
  lbIndex = (lbIndex + 1) % lbImages.length;
  document.getElementById('lbImg').src = lbImages[lbIndex];
});

document.addEventListener('keydown', (e) => {
  const lb = document.getElementById('lightbox');
  if(!lb || !lb.classList.contains('open')) return;
  if(e.key==='Escape') closeLightbox();
  if(e.key==='ArrowLeft'){ lbIndex=(lbIndex-1+lbImages.length)%lbImages.length; document.getElementById('lbImg').src=lbImages[lbIndex]; }
  if(e.key==='ArrowRight'){ lbIndex=(lbIndex+1)%lbImages.length; document.getElementById('lbImg').src=lbImages[lbIndex]; }
});

function closeLightbox() {
  const lb = document.getElementById('lightbox');
  if(lb){ lb.classList.remove('open'); document.body.style.overflow=''; }
}

// ── HERO PARTICLES ─────────────────────────
const canvas = document.getElementById('particles');
if(canvas) {
  const ctx = canvas.getContext('2d');
  let particles = [];
  const resize = () => { canvas.width=window.innerWidth; canvas.height=window.innerHeight; };
  resize();
  window.addEventListener('resize', resize);

  for(let i=0;i<60;i++){
    particles.push({
      x: Math.random()*canvas.width,
      y: Math.random()*canvas.height,
      r: Math.random()*1.5+0.3,
      dx: (Math.random()-0.5)*0.3,
      dy: (Math.random()-0.5)*0.3,
      alpha: Math.random()*0.5+0.1
    });
  }

  function animate(){
    ctx.clearRect(0,0,canvas.width,canvas.height);
    particles.forEach(p=>{
      ctx.beginPath();
      ctx.arc(p.x,p.y,p.r,0,Math.PI*2);
      ctx.fillStyle=`rgba(212,175,55,${p.alpha})`;
      ctx.fill();
      p.x+=p.dx; p.y+=p.dy;
      if(p.x<0||p.x>canvas.width) p.dx*=-1;
      if(p.y<0||p.y>canvas.height) p.dy*=-1;
    });
    requestAnimationFrame(animate);
  }
  animate();
}

// ── COUNTER ANIMATION ──────────────────────
function animateCounter(el, target, suffix='') {
  let count = 0;
  const step = target / 60;
  const timer = setInterval(() => {
    count += step;
    if(count >= target){ count = target; clearInterval(timer); }
    el.textContent = Math.floor(count) + suffix;
  }, 25);
}

const statsObserver = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if(e.isIntersecting){
      const nums = e.target.querySelectorAll('.stat-num');
      nums.forEach(n => {
        const txt = n.textContent.replace(/\D/g,'');
        const suf = n.textContent.replace(/[\d]/g,'');
        if(txt) animateCounter(n, parseInt(txt), suf);
      });
      statsObserver.unobserve(e.target);
    }
  });
}, {threshold:0.5});

const heroStats = document.querySelector('.hero-stats');
if(heroStats) statsObserver.observe(heroStats);

// ── SERVICE CARD HOVER IMAGE SCALE ─────────
document.querySelectorAll('.service-full-card').forEach(card => {
  const img = card.querySelector('img');
  card.addEventListener('mouseenter', () => img && (img.style.transform='scale(1.06)'));
  card.addEventListener('mouseleave', () => img && (img.style.transform=''));
});
