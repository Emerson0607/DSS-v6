// Sidebar functionality
const sideMenu = document.querySelector("aside");
const menuBtn = document.querySelector("#menu-btn");
const closeBtn = document.querySelector("#close-btn");

menuBtn.addEventListener('click', () => {
    sideMenu.style.float = 'left'; // This might not be necessary
    sideMenu.style.display = 'block'; // Show sidebar
});

closeBtn.addEventListener('click', () => {
    sideMenu.style.display = 'none'; // Hide sidebar
});

function getCurrentDateAndDay() {
    const daysOfWeek = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
    const currentDate = new Date();
    const day = currentDate.getDate();
    const month = currentDate.toLocaleString('default', { month: 'long' });
    const year = currentDate.getFullYear();
    const dayOfWeek = daysOfWeek[currentDate.getDay()];

    let daySuffix;
    if (day === 1 || day === 21 || day === 31) {
        daySuffix = "st";
    } else if (day === 2 || day === 22) {
        daySuffix = "nd";
    } else if (day === 3 || day === 23) {
        daySuffix = "rd";
    } else {
        daySuffix = "th";
    }

    const formattedDate = `${day}<span class="small-exponent">${daySuffix}</span> of ${month}, ${dayOfWeek}`;
    return formattedDate;
}


// Display the current date and day in the specified element
const dateContainer = document.getElementById('date-container');
if (dateContainer) {
    dateContainer.innerHTML = getCurrentDateAndDay();
}

// Dropdown functionality
function toggleDropdown() {
    const dropdownContent = document.getElementById('dropdown-content');
    if (dropdownContent) {
        dropdownContent.style.display = (dropdownContent.style.display === 'block') ? 'none' : 'block';
    }
}

// Flashes handling
const flashes = document.querySelectorAll('.flash');
flashes.forEach(function(flash) {
    setTimeout(function() {
        flash.style.opacity = 0;
        flash.style.height = '0';
        flash.style.width = '0';
        flash.style.padding = '0';
        flash.style.margin = '0';
        flash.style.border = 'none';
        flash.addEventListener('transitionend', function() {
            flash.remove();
        });
    }, 3000);
});

// Tooltips (using jQuery)
$(document).ready(function() {
    $('#tooltip, #tooltip2, #tooltip3').hover(function() {
        $(this).find('#tooltipText, #tooltipText2, #tooltipText3').css({
            'top': '-1rem',
            'visibility': 'visible',
            'opacity': '1'
        });
    }, function() {
        $(this).find('#tooltipText, #tooltipText2, #tooltipText3').css({
            'top': '100%',
            'visibility': 'hidden',
            'opacity': '0'
        });
    });

    // Handle login form submission
    $('#upload-form').on('submit', function () {
        document.getElementById('loading-screen').style.display = 'flex';
    });

    $('#upload-form1').on('submit', function () {
        document.getElementById('loading-screen').style.display = 'flex';
    });

    $('.upload_loading').on('submit', function () {
        document.getElementById('loading-screen').style.display = 'flex';
    });
});
 