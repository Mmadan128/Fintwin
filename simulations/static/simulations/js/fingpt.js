let pg1= document.querySelector(".page1")
gsap.from(pg1, {
    y:1000,
    opacity:0,
    duration:1.2,
})
gsap.from(".heading h1, .menu",{
    duration:1,
    y:100,
    opacity:0,
    stagger:0.5,
    delay:0.8
})
gsap.from(".right-container",{
    duration:1,
    x:-500,
    opacity:0,
    delay:1
})
gsap.from(".left-container",{
    duration:1,
    x:500,
    opacity:0,
    delay:1
})
