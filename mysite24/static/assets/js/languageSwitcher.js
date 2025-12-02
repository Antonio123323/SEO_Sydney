(function () {
        function toggleLanguageSwitcher() {
            const languageList = document.getElementById("languageSelect").querySelector('.languageSelect-list');
            if (languageList.classList.contains("show")) {
                languageList.classList.remove("show");
                document.removeEventListener("click", clickOutside);
            } else {
                languageList.classList.add("show");
                document.addEventListener("click", clickOutside);
            }
        }

        function clickOutside(e) {
            console.log("click");
            if (!document.getElementById('languageSelect').contains(e.target)) {
                document.getElementById("languageSelect").querySelector('.languageSelect-list').classList.remove("show");
                document.removeEventListener("click", clickOutside);
                
            }
        }

        if(!!document.querySelector('.languageSelect-toggle')) document.getElementById('languageSelect').querySelector('.languageSelect-toggle').addEventListener('click', toggleLanguageSwitcher);
    }
)()
