var typed = new Typed(".multiple-text", {
    strings: ["Rittikiat Keumyarach","1640700140","Section 327D"],
    typeSpeed: 100,
    backSpeed: 100,
    backDelay: 1000,
    loop: true
})

document.querySelectorAll('.prevNext a, .bullets a').forEach(link => {
    link.addEventListener('click', function(e) {
        e.preventDefault(); // ป้องกันเหตุการณ์เริ่มต้นที่อาจเลื่อนหน้าจอ
        const target = this.getAttribute('data-target'); // ใช้ data-target แทน href

        // ตรวจสอบและอัปเดตสไลด์ตาม target
        if (target === 'next') {
            currentSlide = (currentSlide + 1) % slides.length; // หมุนวนไปยังสไลด์ถัดไป
        } else if (target === 'prev') {
            currentSlide = (currentSlide - 1 + slides.length) % slides.length; // หมุนวนไปยังสไลด์ก่อนหน้า
        } else {
            currentSlide = parseInt(target); // ตรงไปยังสไลด์ที่กำหนด
        }
        updateSlidePosition();
    });
});

function updateSlidePosition() {
    const slider = document.querySelector('.slider');
    slider.style.transform = `translateX(${-100 * currentSlide}%)`;
    updateBullets();
}

function updateBullets() {
    document.querySelectorAll('.bullets a').forEach((bullet, index) => {
        bullet.classList.toggle('active', index === currentSlide);
    });
}