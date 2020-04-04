eggsBasket = {
    1 : "yolo",
    2 : "yolo2",
    3 : "yolo3",
    4 : "yolo4",
    5 : "yolo5",
    6 : "yolo6",
    7 : "yolo7",
    8 : "yolo8",
    9 : "yolo9",
    10 : "yolo10",
    11 : "yolo11",
    12 : "yolo12",
    13 : "yolo13",
    14 : "yolo15",
};

easterEggs = document.querySelector('#easter-eggs');
easterEggs.innerHTML = eggsBasket[Math.floor(Math.random() * 14)];