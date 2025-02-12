function locomotive() {
    gsap.registerPlugin(ScrollTrigger);

    // Initialize LocomotiveScroll
    const locoScroll = new LocomotiveScroll({
        el: document.querySelector(".main"),
        smooth: true
    });

    // ScrollTrigger and LocomotiveScroll setup
    locoScroll.on("scroll", ScrollTrigger.update);
    ScrollTrigger.scrollerProxy(".main", {
        scrollTop(value) {
            return arguments.length ? locoScroll.scrollTo(value, 0, 0) : locoScroll.scroll.instance.scroll.y;
        },
        getBoundingClientRect() {
            return { top: 0, left: 0, width: window.innerWidth, height: window.innerHeight };
        },
        pinType: document.querySelector(".main").style.transform ? "transform" : "fixed"
    });

    // Refresh ScrollTrigger and update on page load
    ScrollTrigger.addEventListener("refresh", () => locoScroll.update());
    ScrollTrigger.refresh();
}
locomotive();

function loader() {
    let num = document.querySelector(".journey span");
    let button = document.querySelector(".journey button");
    let loader = document.querySelector(".loader");
    let g = 0;
    let d = 0;

    // GSAP animations for elements
    gsap.from(".fin, .loader h2", {
        duration: 1,
        y: 100,
        opacity: 0,
        stagger: 0.2
    });
    gsap.from(".journey h3", {
        duration: 1,
        x: -200,
        opacity: 0,
        stagger: 0.2
    });
    gsap.from(".journey button", {
        duration: 1,
        x: 200,
        opacity: 0,
        stagger: 0.2
    });

    // Progress bar logic
    setInterval(function () {
        if (g <= 100) {
            num.innerHTML = g;
            g++;
            if (g === 100) {
                button.innerHTML = "GO AHEAD!";
                d = d + 1;
            }
        }
    }, 25);

    // Button click action to hide loader and show page content
    button.addEventListener("click", function () {
        gsap.to(loader, {
            duration: 0.8,
            y: -1000,
            opacity: 0,
            display: "none"
        });
        gsap.from(".page1, .nav", {
            duration: 1,
            delay: 0.7,
            y: 500,
            opacity: 0
        });
        gsap.from(".nav h1, .nav img, .menu a", {
            duration: 1,
            y: 100,
            delay: 1,
            opacity: 0,
            stagger: 0.2
        });
        gsap.from(".bx1", {
            duration: 1,
            x: -400,
            delay: 1,
            opacity: 0
        });
        gsap.from(".bx2, .bx3", {
            duration: 1,
            x: 400,
            delay: 1,
            opacity: 0
        });
    });
}
loader();

function aim() {
    let vid1 = document.querySelector(".box1 video");
    let box1 = document.querySelector(".box1");
    let moveHandler1 = (dets) => {
        gsap.to(vid1, { x: dets.x, y: dets.y - 400 });
    };
    box1.addEventListener("mouseenter", () => {
        vid1.style.display = "block";
        document.addEventListener("mousemove", moveHandler1);
    });
    box1.addEventListener("mouseleave", () => {
        vid1.style.display = "none";
        document.removeEventListener("mousemove", moveHandler1);
    });

    let vid2 = document.querySelector(".box2 video");
    let box2 = document.querySelector(".box2");
    let moveHandler2 = (dets) => {
        gsap.to(vid2, { x: dets.x, y: dets.y - 500 });
    };
    box2.addEventListener("mouseenter", () => {
        vid2.style.display = "block";
        document.addEventListener("mousemove", moveHandler2);
    });
    box2.addEventListener("mouseleave", () => {
        vid2.style.display = "none";
        document.removeEventListener("mousemove", moveHandler2);
    });

    let vid3 = document.querySelector(".box3 video");
    let box3 = document.querySelector(".box3");
    let moveHandler3 = (dets) => {
        gsap.to(vid3, { x: dets.x, y: dets.y - 500 });
    };
    box3.addEventListener("mouseenter", () => {
        vid3.style.display = "block";
        document.addEventListener("mousemove", moveHandler3);
    });
    box3.addEventListener("mouseleave", () => {
        vid3.style.display = "none";
        document.removeEventListener("mousemove", moveHandler3);
    });
}
aim();
