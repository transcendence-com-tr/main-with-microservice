(function () {
    const gameModes = document.querySelector('.modes');
    const modeCards = document.querySelectorAll('.mode-card');
    let activeIndex = 1;
    let translateX = 0;

    function updateActiveCard() {
        modeCards.forEach(card => {
            card.classList.remove('active', 'neon-blue-force');
        });
        modeCards[activeIndex].classList.add('active', 'neon-blue-force');
        if (modeCards[activeIndex].style.display === 'none')
        {
            modeCards.forEach(card => {
                card.style.display = 'none';
            });
            modeCards[activeIndex].style.display = 'block';
        }
    }

    document.querySelector('.game-modes .fa-chevron-left').parentElement.addEventListener('click', () => {
        if (activeIndex > 0)
        {
            activeIndex--;
            //translateX += modeCards[0].clientWidth;
            //gameModes.style.transform = `translateX(${translateX}px)`;
            gameModes.style.transition = 'transform 0.3s ease';
            updateActiveCard();
        }
    });

    document.querySelector('.game-modes .fa-chevron-right').parentElement.addEventListener('click', () => {
        if (activeIndex < modeCards.length - 1) {
            activeIndex++;
            //translateX -= modeCards[0].clientWidth;
            //gameModes.style.transform = `translateX(${translateX}px)`;
            gameModes.style.transition = 'transform 0.3s ease';
            updateActiveCard();
        }
    });

    updateActiveCard();
})();