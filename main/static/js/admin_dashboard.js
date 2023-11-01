const sideMenu = document.querySelector("aside");
const menuBtn = document.querySelector("#menu-btn");
const closeBtn = document.querySelector("#close-btn");


//show sidebar
menuBtn.addEventListener('click', () => {
    sideMenu.style.float ='left';
    sideMenu.style.display ='block';
   
})

//close sidebar
closeBtn.addEventListener('click', () => {
    sideMenu.style.display = 'none';
})


 // Function to get the current date and day
 function getCurrentDateAndDay() {
    const daysOfWeek = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
    const currentDate = new Date();
    const day = currentDate.getDate();
    const month = currentDate.toLocaleString('default', { month: 'long' });
    const year = currentDate.getFullYear();
    const dayOfWeek = daysOfWeek[currentDate.getDay()];

    const formattedDate = `${day}<span class="small-exponent">th</span> of ${month}, ${dayOfWeek}`;
    return formattedDate;
}

// Display the current date and day in the specified element
const dateContainer = document.getElementById('date-container');
dateContainer.innerHTML = getCurrentDateAndDay();

  // Function to toggle the dropdown
  function toggleDropdown() {
    const dropdownContent = document.getElementById('dropdown-content');
    if (dropdownContent.style.display === 'block') {
        dropdownContent.style.display = 'none';
    } else {
        dropdownContent.style.display = 'block';
    }
}
