// שומר את מיקום הגלילה לפני See More
const seeMoreForm = document.querySelector(".see-more-form");

if (seeMoreForm) {
    seeMoreForm.addEventListener("submit", function () {
        sessionStorage.setItem("scrollPosition", window.scrollY);
    });
}


// מחזיר את המשתמש למיקום הקודם אחרי טעינת הדף
window.addEventListener("load", function () {
    const savedPosition = sessionStorage.getItem("scrollPosition");

    if (savedPosition !== null) {
        window.scrollTo({
            top: parseInt(savedPosition),
            behavior: "smooth"
        });

        sessionStorage.removeItem("scrollPosition");
    }
});


// יוצר מסך Loading
function createLoadingScreen() {
    const loadingScreen = document.createElement("div");

    loadingScreen.id = "loading-screen";
    loadingScreen.innerHTML = `
        <div class="loader-box">
            <div class="loader"></div>
            <p>Loading latest news...</p>
        </div>
    `;

    document.body.appendChild(loadingScreen);
}


// מציג את מסך ה-Loading
function showLoadingScreen() {
    let loadingScreen = document.getElementById("loading-screen");

    if (!loadingScreen) {
        createLoadingScreen();
        loadingScreen = document.getElementById("loading-screen");
    }

    loadingScreen.style.display = "flex";
}


// מוסיף CSS של Loading דרך JavaScript
const loadingStyle = document.createElement("style");

loadingStyle.innerHTML = `
    #loading-screen {
        position: fixed;
        inset: 0;
        background: rgba(15, 23, 42, 0.92);
        display: none;
        align-items: center;
        justify-content: center;
        z-index: 9999;
        color: white;
        backdrop-filter: blur(8px);
    }

    .loader-box {
        text-align: center;
        font-family: Arial, sans-serif;
    }

    .loader {
        width: 48px;
        height: 48px;
        border: 5px solid rgba(255,255,255,0.2);
        border-top: 5px solid #38bdf8;
        border-radius: 50%;
        animation: spin 0.9s linear infinite;
        margin: 0 auto 18px auto;
    }

    .loader-box p {
        font-size: 1.1rem;
        color: #e2e8f0;
        font-weight: 600;
    }

    @keyframes spin {
        from {
            transform: rotate(0deg);
        }

        to {
            transform: rotate(360deg);
        }
    }
`;

document.head.appendChild(loadingStyle);


// מציג Loading לכל form רגיל
document.querySelectorAll("form").forEach(function (form) {

    // לא מציג Loading לשמירת כתבה שעובדת בתוך iframe נסתר
    if (form.target && form.target.includes("hidden_save_frame")) {
        return;
    }

    form.addEventListener("submit", function () {
        showLoadingScreen();
    });
});