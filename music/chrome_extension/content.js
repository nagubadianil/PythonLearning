let clickInterval;
let clickEnabled = false;
let mouse_event = "mouseenter";
let run_buttons = null;
let run_button_index = 0;
let code_boxes = null
let which_box = 0


// Function to find an element containing specific text
function findElementByText(text) {
  const elements = document.querySelectorAll("*");
  for (let element of elements) {
    if (element.textContent.includes(text)) {
      return element;
    }
  }
  return null;
}

// Function to get the center coordinates of an element
function getCenterCoordinates(element) {
  const rect = element.getBoundingClientRect();
  const centerX = rect.left + rect.width / 2;
  const centerY = rect.top + rect.height / 2;
  return { x: centerX, y: centerY };
}

function createMouseEvent(type, element) {
  const mouseEvent = new MouseEvent(type, {
    bubbles: true,
    cancelable: true,
    view: window,
    clientX: element.getBoundingClientRect().left + element.offsetWidth / 2,
    clientY: element.getBoundingClientRect().top + element.offsetHeight / 2,
  });

  element.dispatchEvent(mouseEvent);
}
// Function to simulate a mouse click at a specific position
function simulateClick(x, y) {
  //console.log(`simulate Click ${x} ${y}`);
  const event = new MouseEvent("click", {
    bubbles: true,
    cancelable: true,
    clientX: x,
    clientY: y,
  });
  document.elementFromPoint(x, y)?.dispatchEvent(event);
}
function findLastElementWithClasses() {
  const elements = document.querySelectorAll(
    ".cell.code.icon-scrolling.focused"
  );
  return elements.length > 0 ? elements[elements.length - 1] : null;
}

// Start random clicking on the element containing the specified text
function startClicking() {
  clickEnabled = true;
  code_boxes = document.querySelectorAll('.editor.flex.lazy-editor');
  which_box = 0
  //debugger
  let box1 = getCenterCoordinates(code_boxes[code_boxes.length -1]);
  console.log(`Got X1,Y1 = (${box1.x}, ${box1.y})`);
  
  let box2 = getCenterCoordinates(code_boxes[code_boxes.length -2]);
  console.log(`Got X2,Y2 = (${box2.x}, ${box2.y})`);
   
  // Start clicking at the element's center
  clickInterval = setInterval(() => {
    if (clickEnabled) {
      if(which_box == 0){
        console.log("Clicking in Last code box!")
        simulateClick(box1.x, box1.y);
        simulateClick(box1.x-20, box1.y);
        which_box = 1
      }
      else {
        console.log("Clicking in Second Last code box!")
        simulateClick(box2.x, box2.y);
        simulateClick(box2.x-20, box2.y);
        which_box = 0
      }
      
    }
  }, 1000);
}

// Stop random clicking
function stopClicking() {
  clickEnabled = false;
  clearInterval(clickInterval);
}

// Event listeners for enabling/disabling the clicker
chrome.runtime.onMessage.addListener((message) => {
  if (message.action === "startClicking") {
    console.log("startClicking");
    startClicking();
  } else if (message.action === "stopClicking") {
    console.log("stopClicking");
    stopClicking();
  }

  if (message.action === "startScrolling") {
    console.log("startScrolling");
    startScrolling();
  } else if (message.action === "stopScrolling") {
    console.log("stopScrolling");
    stopScrolling();
  }
});

let scrollDirection = "down"; // Keep track of the current direction
let scrollInterval;
let scrollEnabled = false;
// Function to scroll half a page
function scrollHalfPage() {
  const scrollAmount = window.innerHeight; // Half the viewport height
  if (scrollDirection === "down") {
    console.log("......scrolling down");
    window.scrollBy(0, scrollAmount);
    scrollDirection = "up"; // Change direction to up
  } else {
    console.log("......scrolling up");
    window.scrollBy(0, -scrollAmount);
    scrollDirection = "down"; // Change direction to down
  }
}

// Function to start alternating scrolling
function startScrolling() {
  scrollEnabled = true;

  run_buttons = document.querySelectorAll(".cell-execution-container");

  run_button_index = run_buttons.length - 1;

  scrollInterval = setInterval(() => {
    if (scrollEnabled) {
      console.log(`mouseeven: ${mouse_event}`);
      //scrollHalfPage();
      
      createMouseEvent(mouse_event, run_buttons[run_button_index]);

      if (mouse_event == "mouseleave") {
        if (run_button_index == run_buttons.length -3) {
          run_button_index = run_buttons.length - 1;
        } else {
          run_button_index = run_button_index - 1;
        }
      }
      mouse_event = mouse_event == "mouseleave" ? "mouseenter" : "mouseleave";
    }
  }, 1000); // Scroll every 1 second
}

// Stop scrolling
function stopScrolling() {
  scrollEnabled = false;
  clearInterval(scrollInterval);
}

// notebook-cell-list -- last child of this class
//cell-gutter  -- last of these
//cell-execution-container  -- last of these
// element colab-run-button
//editor flex lazy-editor
// document.querySelectorAll('.editor.flex.lazy-editor');