(() => {
  const menuButton = document.querySelector(".menu-toggle");
  const nav = document.querySelector("#main-nav");

  if (menuButton && nav) {
    menuButton.addEventListener("click", () => {
      const open = menuButton.getAttribute("aria-expanded") !== "true";
      menuButton.setAttribute("aria-expanded", String(open));
      menuButton.setAttribute("aria-label", open ? "Close navigation" : "Open navigation");
      nav.classList.toggle("is-open", open);
    });

    nav.querySelectorAll("a").forEach((link) => {
      link.addEventListener("click", () => {
        menuButton.setAttribute("aria-expanded", "false");
        menuButton.setAttribute("aria-label", "Open navigation");
        nav.classList.remove("is-open");
      });
    });
  }

  const views = {
    industry: {
      title: "INDUSTRY OVERVIEW / DASHBOARD EXPORT",
      caption: "Industry Overview",
      image: "https://raw.githubusercontent.com/karanveersingh05/MutualFundsAnalytics/main/dashboard/Page_1_Industry_Overview.png",
      link: "https://github.com/karanveersingh05/MutualFundsAnalytics/blob/main/dashboard/Page_1_Industry_Overview.png",
      alt: "Industry overview dashboard export from the project"
    },
    performance: {
      title: "FUND PERFORMANCE / DASHBOARD EXPORT",
      caption: "Fund Performance",
      image: "https://raw.githubusercontent.com/karanveersingh05/MutualFundsAnalytics/main/dashboard/Page_2_Fund_Performance.png",
      link: "https://github.com/karanveersingh05/MutualFundsAnalytics/blob/main/dashboard/Page_2_Fund_Performance.png",
      alt: "Fund performance dashboard export from the project"
    },
    investor: {
      title: "INVESTOR ANALYTICS / DASHBOARD EXPORT",
      caption: "Investor Analytics",
      image: "https://raw.githubusercontent.com/karanveersingh05/MutualFundsAnalytics/main/dashboard/Page_3_Investor_Analytics.png",
      link: "https://github.com/karanveersingh05/MutualFundsAnalytics/blob/main/dashboard/Page_3_Investor_Analytics.png",
      alt: "Investor analytics dashboard export from the project"
    },
    sip: {
      title: "SIP MARKET TRENDS / DASHBOARD EXPORT",
      caption: "SIP & Market Trends",
      image: "https://raw.githubusercontent.com/karanveersingh05/MutualFundsAnalytics/main/dashboard/Page_4_SIP_Market_Trends.png",
      link: "https://github.com/karanveersingh05/MutualFundsAnalytics/blob/main/dashboard/Page_4_SIP_Market_Trends.png",
      alt: "SIP and market trends dashboard export from the project"
    }
  };

  const tabs = [...document.querySelectorAll(".dashboard-tab")];
  const image = document.querySelector("#dashboard-image");
  const imageFallback = document.querySelector("#image-fallback");
  const previewTitle = document.querySelector("#preview-title");
  const previewCaption = document.querySelector("#preview-caption");
  const previewLink = document.querySelector("#preview-link");

  function selectView(key) {
    const view = views[key];
    if (!view || !image) return;

    tabs.forEach((tab) => {
      const active = tab.dataset.view === key;
      tab.classList.toggle("is-active", active);
      tab.setAttribute("aria-selected", String(active));
      tab.tabIndex = active ? 0 : -1;
    });

    image.hidden = false;
    imageFallback.hidden = true;
    image.alt = view.alt;
    image.src = view.image;
    previewTitle.textContent = view.title;
    previewCaption.textContent = view.caption;
    previewLink.href = view.link;
  }

  tabs.forEach((tab) => {
    tab.addEventListener("click", () => selectView(tab.dataset.view));
    tab.addEventListener("keydown", (event) => {
      if (event.key !== "ArrowRight" && event.key !== "ArrowLeft") return;
      event.preventDefault();
      const index = tabs.indexOf(tab);
      const next = (index + (event.key === "ArrowRight" ? 1 : -1) + tabs.length) % tabs.length;
      tabs[next].focus();
      selectView(tabs[next].dataset.view);
    });
  });

  if (image) {
    image.addEventListener("error", () => {
      image.hidden = true;
      imageFallback.hidden = false;
    });
  }

  tabs.forEach((tab, index) => { tab.tabIndex = index === 0 ? 0 : -1; });
})();
