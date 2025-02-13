const scroll = new LocomotiveScroll({
    el: document.querySelector('.main'),
    smooth: true
});
gsap.from(".main",{
    y:1000,
    opacity:0,
    duration:1.2,
})