let clickEnabled = false;
let scrollEnabled = false;

document.addEventListener("DOMContentLoaded", function () {
  loadState();
  // Your initialization code here
});

function loadState()  {
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    const currentTab = tabs[0];
    //alert(`tab: ${currentTab.id} title: ${currentTab.title}`)    
    
    chrome.tabs.sendMessage(tabs[0].id, { action: "sendState", data: currentTab.id});
 
    chrome.runtime.onMessage.addListener((message) => {
      if (message.action === "currentState") {
        let state = message.data;
        
        if (state.id == currentTab.id){
        
        //alert(`SAME TAB: click ${state.clickEnabled} scroll ${state.clickEnabled}`);

        const scrollEnabled = state.scrollEnabled;
        const clickEnabled = state.clickEnabled;

        setClickButtonState(clickEnabled);
        setScrollButtonState(scrollEnabled);
        }
      }
    });
  });

}

  //window.onLoad = loadState

function updateState(stateName, value) {
    let state = {};
    state[stateName] = value;
    chrome.storage.local.set(state, function() {
      console.log(`${stateName} set to ${value}`);
    });
  }


function setScrollButtonState(scrollEnabled)
{
    let elem = document.getElementById('toggleScroll')
    elem.innerHTML = scrollEnabled ? "Disable Scroll" : "Enable Scroll";
    elem.className =  scrollEnabled ? "ToggleButtonEnabled" : "ToggleButton";
}   

function setClickButtonState(clickEnabled)
{
    let elem = document.getElementById('toggleClick')
    elem.innerHTML = clickEnabled ? "Disable Click" : "Enable Click";
    elem.className =  clickEnabled ? "ToggleButtonEnabled" : "ToggleButton";
}   
document.getElementById("toggleClick").addEventListener("click", () => {
    clickEnabled = !clickEnabled;
    
    updateState('clickEnabled', clickEnabled);
    
    const action = clickEnabled ? "startClicking" : "stopClicking";
    setClickButtonState(clickEnabled)
  
      chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        if (tabs[0]?.id) {
          chrome.scripting
            .executeScript({
              target: { tabId: tabs[0].id },
              files: ["content.js"],
            })
            .then(() => {
              if (clickEnabled) {
                chrome.tabs.sendMessage(tabs[0].id, { action: "startClicking" });
              } else {
                chrome.tabs.sendMessage(tabs[0].id, { action: "stopClicking" });
              }
            })
            .catch((error) => {
              console.error("Error injecting content script:", error);
            });
        } else {
          console.error("No active tab found.");
        }
      });
  
  });

  document.getElementById("toggleScroll").addEventListener("click", () => {
    scrollEnabled = !scrollEnabled;
    
    updateState('scrollEnabled', scrollEnabled);

    const action = scrollEnabled ? "startScrolling" : "stopScrolling";
    setScrollButtonState(scrollEnabled)
  
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      if (tabs[0]?.id) {
        chrome.scripting
          .executeScript({
            target: { tabId: tabs[0].id },
            files: ["content.js"],
          })
          .then(() => {
            if (scrollEnabled) {
              chrome.tabs.sendMessage(tabs[0].id, { action: "startScrolling" });
            } else {
              chrome.tabs.sendMessage(tabs[0].id, { action: "stopScrolling" });
            }
          })
          .catch((error) => {
            console.error("Error injecting content script:", error);
          });
      } else {
        console.error("No active tab found.");
      }
    });
  });

//   document.getElementById("toggleScroll").addEventListener("click", () => {
//     chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
//       if (tabs[0]?.id) {
//         chrome.scripting.executeScript({
//           target: { tabId: tabs[0].id },
//           files: ["content.js"],
//         }).then(() => {
//           chrome.tabs.sendMessage(tabs[0].id, { action: "startScrolling" });
//         }).catch((error) => {
//           console.error("Error injecting content script:", error);
//         });
//       } else {
//         console.error("No active tab found.");
//       }
//     });
//   });