// 漫画灰博客 · 前端交互
(function () {
  "use strict";

  var reduced = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // 星空背景渲染（纯 Canvas，无外部依赖，单色灰白星点 + 流星）
  function initStarfield(canvas) {
    if (!canvas) return;
    var ctx = canvas.getContext("2d");
    var stars = [];
    var shooting = [];

    // 鼠标跟随状态
    var hasMouse = false;
    var cx = 0, cy = 0;             // 光标像素坐标
    var px = 0, py = 0, tx = 0, ty = 0; // 平滑视差偏移（归一化 -0.5..0.5）

    function dims() {
      return {
        w: canvas.clientWidth || window.innerWidth,
        h: canvas.clientHeight || window.innerHeight
      };
    }

    function resize() {
      var dpr = window.devicePixelRatio || 1;
      var d = dims();
      canvas.width = d.w * dpr;
      canvas.height = d.h * dpr;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      makeStars();
    }

    function makeStars() {
      var d = dims();
      var count = Math.min(260, Math.floor((d.w * d.h) / 3200));
      stars = [];
      for (var i = 0; i < count; i++) {
        var big = Math.random() < 0.06; // 约 6% 大颗亮星
        stars.push({
          x: Math.random() * d.w,
          y: Math.random() * d.h,
          r: big ? Math.random() * 1.2 + 2.2 : Math.random() * 1.7 + 0.5,
          base: Math.random() * 0.5 + 0.4,
          phase: Math.random() * Math.PI * 2,
          twinkle: Math.random() * 0.02 + 0.006,
          drift: Math.random() * 0.06 + 0.012,
          depth: Math.random() * 0.85 + 0.15,
          glow: big
        });
      }
    }

    function spawnShoot() {
      var d = dims();
      shooting.push({
        x: Math.random() * d.w,
        y: Math.random() * d.h * 0.4,
        vx: (Math.random() * 3 + 3) * (Math.random() < 0.5 ? 1 : -1),
        vy: Math.random() * 2 + 2,
        life: 1
      });
    }

    var shootTimer = 0;

    function frame() {
      if (!document.body.contains(canvas)) return; // 封面移除后停止渲染
      var d = dims();
      ctx.clearRect(0, 0, d.w, d.h);

      // 平滑跟随鼠标（视差）
      px += (tx - px) * 0.08;
      py += (ty - py) * 0.08;

      var R = 150; // 连线半径

      // 光标柔光
      if (!reduced && hasMouse) {
        var glow = ctx.createRadialGradient(cx, cy, 0, cx, cy, R);
        glow.addColorStop(0, "rgba(255, 255, 255, 0.06)");
        glow.addColorStop(1, "rgba(255, 255, 255, 0)");
        ctx.fillStyle = glow;
        ctx.fillRect(cx - R, cy - R, R * 2, R * 2);
      }

      var nearest = null;
      var nearestDist = Infinity;

      // 画星星：视差 + 靠近光标时被轻微吸引并变亮
      for (var i = 0; i < stars.length; i++) {
        var s = stars[i];
        s.phase += s.twinkle;
        s.x += s.drift;
        if (s.x > d.w + 2) s.x = -2;
        if (s.x < -2) s.x = d.w + 2;

        var sx = s.x + s.depth * px * 55;
        var sy = s.y + s.depth * py * 55;

        s.near = false;
        if (!reduced && hasMouse) {
          var ddx = sx - cx, ddy = sy - cy;
          var dist = Math.sqrt(ddx * ddx + ddy * ddy);
          if (dist < R) {
            s.near = true;
            s.dist = dist;
            var pull = 1 - dist / R;
            sx += (cx - sx) * pull * 0.05;
            sy += (cy - sy) * pull * 0.05;
            if (dist < nearestDist) { nearestDist = dist; nearest = s; }
          }
        }
        s.sx = sx;
        s.sy = sy;

        var a = Math.max(0, Math.min(1, s.base + Math.sin(s.phase) * 0.3));
        if (s.near) a = Math.min(1, a + 0.45);

        // 大颗亮星的柔光
        if (s.glow) {
          ctx.globalAlpha = a * 0.35;
          ctx.fillStyle = "#ffffff";
          ctx.beginPath();
          ctx.arc(sx, sy, s.r * 2.6, 0, Math.PI * 2);
          ctx.fill();
        }

        ctx.globalAlpha = a;
        ctx.fillStyle = "#ffffff";
        ctx.beginPath();
        ctx.arc(sx, sy, s.r, 0, Math.PI * 2);
        ctx.fill();
      }

      // 连线：光标 → 附近星星，最近那颗朱砂红且更实
      if (!reduced && hasMouse) {
        for (var k = 0; k < stars.length; k++) {
          var s2 = stars[k];
          if (!s2.near) continue;
          var t = 1 - s2.dist / R;
          var isNearest = (s2 === nearest);
          ctx.globalAlpha = isNearest ? 0.55 * t + 0.12 : 0.30 * t;
          ctx.lineWidth = isNearest ? 1.4 : 1;
          ctx.strokeStyle = isNearest ? "#d96b4e" : "#ffffff";
          ctx.beginPath();
          ctx.moveTo(cx, cy);
          ctx.lineTo(s2.sx, s2.sy);
          ctx.stroke();
        }

        // 光标节点：白点 + 朱砂红小环
        ctx.globalAlpha = 0.9;
        ctx.fillStyle = "#ffffff";
        ctx.beginPath();
        ctx.arc(cx, cy, 2, 0, Math.PI * 2);
        ctx.fill();
        ctx.globalAlpha = 0.5;
        ctx.strokeStyle = "#d96b4e";
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.arc(cx, cy, 6, 0, Math.PI * 2);
        ctx.stroke();
      }

      // 流星
      if (!reduced) {
        shootTimer -= 16;
        if (shootTimer <= 0) { spawnShoot(); shootTimer = Math.random() * 4200 + 1800; }
        for (var j = shooting.length - 1; j >= 0; j--) {
          var m = shooting[j];
          m.x += m.vx;
          m.y += m.vy;
          m.life -= 0.02;
          if (m.life <= 0 || m.x < -60 || m.x > d.w + 60 || m.y > d.h + 60) {
            shooting.splice(j, 1);
            continue;
          }
          ctx.globalAlpha = Math.max(0, m.life);
          ctx.strokeStyle = "#ffffff";
          ctx.lineWidth = 1;
          ctx.beginPath();
          ctx.moveTo(m.x, m.y);
          ctx.lineTo(m.x - m.vx * 9, m.y - m.vy * 9);
          ctx.stroke();
        }
      }

      ctx.globalAlpha = 1;
      requestAnimationFrame(frame);
    }

    if (!reduced) {
      window.addEventListener("mousemove", function (e) {
        var d = dims();
        hasMouse = true;
        cx = e.clientX;
        cy = e.clientY;
        tx = cx / d.w - 0.5;
        ty = cy / d.h - 0.5;
      });
    }

    resize();
    window.addEventListener("resize", resize);
    requestAnimationFrame(frame);
  }

  // 0. 加载进入页（Splash）：星空 + 动态进度 → 「进入」按钮 → 点击淡出
  var splash = document.getElementById("splash");
  if (splash) {
    var html = document.documentElement;
    if (html.classList.contains("splash-done")) {
      splash.remove();
    } else {
      initStarfield(document.getElementById("splash-canvas"));
      var fill = document.getElementById("splash-fill");
      var pct = document.getElementById("splash-percent");
      var enter = document.getElementById("splash-enter");
      var progress = 0;
      var timer = setInterval(function () {
        progress += Math.random() * 3 + 1; // 随机增速，更接近真实加载
        if (progress >= 100) {
          progress = 100;
          clearInterval(timer);
          enter.classList.add("show");
        }
        fill.style.width = progress + "%";
        pct.textContent = Math.floor(progress);
      }, 40);

      enter.addEventListener("click", function () {
        try { sessionStorage.setItem("splash_done", "1"); } catch (e) {}
        splash.classList.add("fade-out");
        setTimeout(function () { splash.remove(); }, 620);
      });
    }
  }

  // 1. 滚动入场（IntersectionObserver，同容器内兄弟元素错峰）
  var revealEls = document.querySelectorAll(".reveal");
  if (revealEls.length) {
    if ("IntersectionObserver" in window) {
      revealEls.forEach(function (el) {
        var sibs = Array.prototype.filter.call(el.parentElement.children, function (c) {
          return c.classList && c.classList.contains("reveal");
        });
        var idx = sibs.indexOf(el);
        if (idx > 0) el.style.transitionDelay = Math.min(idx, 8) * 0.06 + "s";
      });
      var io = new IntersectionObserver(
        function (entries) {
          entries.forEach(function (entry) {
            if (entry.isIntersecting) {
              entry.target.classList.add("is-visible");
              io.unobserve(entry.target);
            }
          });
        },
        { threshold: 0.12, rootMargin: "0px 0px -40px 0px" }
      );
      revealEls.forEach(function (el) { io.observe(el); });
    } else {
      revealEls.forEach(function (el) { el.classList.add("is-visible"); });
    }
  }

  // 2. 深色 / 浅色切换
  var themeToggle = document.getElementById("theme-toggle");
  if (themeToggle) {
    themeToggle.addEventListener("click", function () {
      var h = document.documentElement;
      var next = h.getAttribute("data-theme") === "dark" ? "light" : "dark";
      h.setAttribute("data-theme", next);
      try { localStorage.setItem("theme", next); } catch (e) {}
    });
  }

  // 3. 顶栏滚动阴影
  var header = document.querySelector(".site-header");
  if (header) {
    var onHeaderScroll = function () {
      if (window.scrollY > 8) header.classList.add("scrolled");
      else header.classList.remove("scrolled");
    };
    window.addEventListener("scroll", onHeaderScroll, { passive: true });
    onHeaderScroll();
  }

  // 4. 移动端导航折叠
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.querySelector(".nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      nav.classList.toggle("open");
    });
  }

  // 5. 阅读进度条
  var progressBar = document.getElementById("reading-progress");
  if (progressBar) {
    var updateProgress = function () {
      var doc = document.documentElement;
      var scrollable = doc.scrollHeight - doc.clientHeight;
      var p = scrollable > 0 ? doc.scrollTop / scrollable : 0;
      progressBar.style.transform = "scaleX(" + p + ")";
    };
    window.addEventListener("scroll", updateProgress, { passive: true });
    updateProgress();
  }

  // 6. 回到顶部
  var backTop = document.getElementById("back-top");
  if (backTop) {
    var onBackScroll = function () {
      if (window.scrollY > 400) backTop.classList.add("show");
      else backTop.classList.remove("show");
    };
    window.addEventListener("scroll", onBackScroll, { passive: true });
    backTop.addEventListener("click", function () {
      window.scrollTo({ top: 0, behavior: reduced ? "auto" : "smooth" });
    });
    onBackScroll();
  }

  // 7. 评论回复：点击「回复」填入父评论 id 并滚动到表单
  var replyButtons = document.querySelectorAll(".comment-reply");
  var parentField = document.querySelector("#id_parent_id");
  var form = document.querySelector(".comment-form");
  if (replyButtons.length && parentField && form) {
    replyButtons.forEach(function (btn) {
      btn.addEventListener("click", function () {
        parentField.value = btn.getAttribute("data-id") || "";
        form.scrollIntoView({ behavior: reduced ? "auto" : "smooth" });
      });
    });
  }

  // 8. 相册灯箱
  var items = document.querySelectorAll(".gallery-item");
  var lightbox = document.querySelector(".lightbox");
  if (items.length && lightbox) {
    var img = lightbox.querySelector(".lightbox-img");
    var caption = lightbox.querySelector(".lightbox-caption");
    var closeBtn = lightbox.querySelector(".lightbox-close");
    var prevBtn = lightbox.querySelector(".lightbox-prev");
    var nextBtn = lightbox.querySelector(".lightbox-next");
    var current = 0;

    function show(i) {
      current = (i + items.length) % items.length;
      var item = items[current];
      var el = item.querySelector("img");
      img.src = el.getAttribute("data-full") || el.src;
      caption.textContent = el.alt || item.getAttribute("data-title") || "";
    }

    items.forEach(function (item, idx) {
      item.addEventListener("click", function () {
        show(idx);
        lightbox.classList.add("open");
      });
    });

    function close() { lightbox.classList.remove("open"); }

    closeBtn.addEventListener("click", close);
    lightbox.addEventListener("click", function (e) {
      if (e.target === lightbox) close();
    });
    prevBtn.addEventListener("click", function () { show(current - 1); });
    nextBtn.addEventListener("click", function () { show(current + 1); });
    document.addEventListener("keydown", function (e) {
      if (!lightbox.classList.contains("open")) return;
      if (e.key === "Escape") close();
      if (e.key === "ArrowLeft") show(current - 1);
      if (e.key === "ArrowRight") show(current + 1);
    });
  }

  // 9. 作品卡片轻微 3D 倾斜
  if (!reduced) {
    var tiltCards = document.querySelectorAll(".tilt");
    tiltCards.forEach(function (card) {
      card.addEventListener("mousemove", function (e) {
        var r = card.getBoundingClientRect();
        var x = (e.clientX - r.left) / r.width - 0.5;
        var y = (e.clientY - r.top) / r.height - 0.5;
        card.style.transform =
          "perspective(700px) rotateX(" + (-y * 4) + "deg) rotateY(" + (x * 4) + "deg) translateY(-4px)";
      });
      card.addEventListener("mouseleave", function () {
        card.style.transform = "";
      });
    });
  }
})();
