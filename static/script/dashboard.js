document.addEventListener("DOMContentLoaded", () => {
  const menuButton = document.querySelector(".menu-button");
  const menu = document.querySelector(".menu");
  const backButton = document.querySelector(".back-button");

  menuButton.addEventListener("click", () => {
      if (menu.style.right === "0px") {
          menu.style.right = "-250px";
      } else {
          menu.style.right = "0px";
      }
  });

  backButton.addEventListener("click", () => {
      menu.style.right = "-250px";
  });

  document.addEventListener("click", (event) => {
      if (!menu.contains(event.target) && !menuButton.contains(event.target)) {
          menu.style.right = "-250px";
      }
  });
});