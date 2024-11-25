let clickEnabled = false;
let scrollEnabled = false;

document.getElementById("toggleClick").addEventListener("click", () => {
    clickEnabled = !clickEnabled;
  
    const action = clickEnabled ? "startClicking" : "stopClicking";
    document.getElementById("toggleClick").textContent = clickEnabled
      ? "Disable Clicker"
      : "Enable Clicker";
  
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
  
    const action = scrollEnabled ? "startScrolling" : "stopScrolling";
    document.getElementById("toggleScroll").textContent = scrollEnabled
      ? "Disable Scroller"
      : "Enable Scroller";
  
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