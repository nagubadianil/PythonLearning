// Load the extension on popup open
document.addEventListener("DOMContentLoaded", async () => {
  await loadFriendsBookmarks();
  await loadMyBookmarks();
});

document.addEventListener("DOMContentLoaded", async () => {
  // Get stored profile name from chrome storage

  const response = await sendMessageToRuntime({
    action: "initialize",
  });

  if (response && response.status === "success") {
    document.getElementById("profile-name").innerHTML = response.profileName;
  } else {
  }
});

document.getElementById("share-btn").addEventListener("click", async () => {
  const selectedBookmarks = getSelectedBookmarks(
    document.getElementById("bookmark-tree")
  );
  if (selectedBookmarks.length === 0) {
    alert("Please select some bookmarks to share.");
    return;
  }

  const response = await sendMessageToRuntime({
    action: "shareBookmarks",
    profileName: "",
    bookmarks: selectedBookmarks,
  });

  if (response && response.status === "success") {
    console.log("Bookmarks shared successfully!");
    
    document.getElementById("refresh-btn").click()
    // Perform additional success actions here
  } else {
    console.error("Failed to share bookmarks.");
    // Handle failure here
  }
});

document.getElementById("add-btn").addEventListener("click", async () => {
  createBookmarksFromProfiles();
});

document.getElementById("refresh-btn").addEventListener("click", async () => {
  const response = await sendMessageToRuntime({
    action: "fetchAllProfilesBookmarks",
  });

  if (response && response.status === "success") {

    console.log("Fetching all profiles successfull")

    for (const profile of response.bookmarksData) {
      const bookmarkObjectArray = [];
      for (const row of profile.bookmarks) {
        const bookmarkObject = {};
        bookmarkObject.title = row[0];
        bookmarkObject.url = row[1];
        bookmarkObjectArray.push(bookmarkObject);
      }
      profile.bookmarks = createBookmarkStructure(bookmarkObjectArray);
    }
    await setToStorage({
      all_profiles: JSON.stringify(response.bookmarksData),
    });

    await loadFriendsBookmarks();
    await loadMyBookmarks();
  } else {
    alert("Failed to retrieve all bookmarks.");
    // Handle failure here
  }
});

async function loadFriendsBookmarks() {
  const result = await getFromStorage(["all_profiles"]);

  if (!(result && result.all_profiles && result.all_profiles.length)) {
    document.getElementById("refresh-btn").click()
    return;
  }
  let g_all_profiles = JSON.parse(result.all_profiles);

  if (!g_all_profiles) return;

  await calculateCheckedForProfiles(g_all_profiles);

  //await setToStorage({ all_profiles: JSON.stringify(g_all_profiles) });
  //console.log("g_all_profiles:", JSON.stringify(g_all_profiles, null, 2));

  await renderOtherBookmarks(g_all_profiles);
}

function getImmediateCheckboxChildren(parentElement) {
  const checkboxes = [];
  // Traverse the immediate children of the parent element
  for (const child of parentElement.children) {
    // Check if the child is an <input> element of type checkbox
    if (child.tagName === "INPUT" && child.type === "checkbox") {
      checkboxes.push(child);
    }
    // If the child is an <li>, check its direct children
    if (child.tagName === "LI") {
      for (const liChild of child.children) {
        if (liChild.tagName === "INPUT" && liChild.type === "checkbox") {
          checkboxes.push(liChild);
        }
      }
    }
  }
  return checkboxes;
}
// Fetch and display bookmarks from the browser's bookmark bar
async function loadMyBookmarks() {
  chrome.bookmarks.getTree(async (bookmarkTree) => {
    //debugger;
    // Find the Bookmarks Bar
    //const bookmarkBar = bookmarkTree[0].children.find((node) => node.title === "Bookmarks Bar");
    const bookmarkBar = bookmarkTree[0]; //.find((node) => node.title === "Bookmarks Bar");

    const container = document.getElementById("bookmark-tree");

    deleteAllChildren(container);

    const result = await getFromStorage(["all_profiles"]);
    let g_all_profiles = null
    
    if (result && result.all_profiles && result.all_profiles.length) {
      g_all_profiles = JSON.parse(result.all_profiles);
    }
    let bookmarkBarChildren = bookmarkBar.children[0].children;
    if (bookmarkBar.children[0].title == "Bookmarks bar") {
      if (g_all_profiles) {
      await calculateCheckedForMyBookmarks(bookmarkBarChildren, g_all_profiles)
      
        deleteOtherProfilesBookmarks(bookmarkBarChildren, g_all_profiles);
      }
    }

    for (let i = 1; i < bookmarkBar.children.length; i++) {
      bookmarkBar.children.splice(i, 1);
    }

    if (bookmarkBar) {
      // Load bookmarks from the Bookmarks Bar and pre-check them
      createBookmarkTree(bookmarkBar.children, container, true); // Pre-check all bookmarks
    } else {
      container.innerHTML =
        "<p>Rushi, No bookmarks found in the Bookmarks Bar.</p>";
    }
  });
}
function deleteAllChildren(element) {
  while (element.firstChild) {
    element.removeChild(element.firstChild);
  }
}
function deleteOtherProfilesBookmarks(bookmarkBarChildren, g_all_profiles) {
  for (const profile of g_all_profiles) {
    let index = 0;
    for (const child of bookmarkBarChildren) {
      if (child.title == profile.profileName) {
        bookmarkBarChildren.splice(index, 1);
        break;
      }
      index++;
    }
  }
}
async function  calculateCheckedForMyBookmarks(bookmarkBarChildren,g_all_profiles){
  console.log("START calculateCheckedForMyBookmarks")
  const result = await getFromStorage(["profileName", "all_profiles"]);

  if (!(result && result.profileName && result.profileName.length &&
    result.all_profiles && result.all_profiles.length
   ))
    return
    
  let myProfile = null
    for( const profile of g_all_profiles){
      if (profile.profileName == result.profileName)
      {
        myProfile = profile
        console.log("Found my profile!!")
      }
    }

    if (myProfile) {
      const sourceBookmarks = myProfile.bookmarks[0].children; //[0].children;
      const destinationBookmarks = bookmarkBarChildren; //[0].children
      updateCheckedProperty(sourceBookmarks, destinationBookmarks);
    }
  
  console.log("END calculateCheckedForMyBookmarks")
}

function calculateCheckedForProfiles(g_all_profiles) {
  return new Promise((resolve, reject) => {
    chrome.bookmarks.getTree(async (bookmarkTree) => {
      const result = await getFromStorage(["profileName"]);
      const bookmarkBar = bookmarkTree[0];
      let bookmarkBarChildren = bookmarkBar.children[0].children;
      if (bookmarkBar.children[0].title == "Bookmarks bar") {
        for (const profile of g_all_profiles) {
          if (
            result &&
            result.profileName &&
            result.profileName == profile.profileName
          ) {
            continue;
          }

          for (const child of bookmarkBarChildren) {
            if (child.title == profile.profileName) {
              const destinationBookmarks = profile.bookmarks[0].children; //[0].children;
              const sourceBookmarks = child.children; //[0].children
              updateCheckedProperty(sourceBookmarks, destinationBookmarks);
            }
          }
        }
      }
      resolve(true);
    });
  });
}
function updateCheckedProperty(source, destination) {
  if (!destination || !destination?.length) return;
  console.log(
    `updateCheckedProperty beg destination length: ${destination?.length}`
  );

  let matched = 0;
  for (const destItem of destination) {
    // Check if a matching item exists in the source hierarchy at the same level
    // const matchingSource = source.find(
    //   (srcItem) => srcItem.title === destItem.title
    // );

    let matchingSource = null;

    let leaf = "FOLDER";
    if (!(destItem.children && destItem.children.length)) {
      leaf = "LEAF";
    }

    //console.log(`---DEST Comparing ${leaf} ${destItem.title}`);
    for (const srcItem of source) {
      //console.log(`-----SRC Comparing ${srcItem.title}`);
      if (destItem.title.trim() == srcItem.title.trim()) {
        matchingSource = srcItem;

        //console.log("     $$$ Match found!!");
        break;
      }
    }

    // If a match is found, set the `checked` property to true
    if (matchingSource) {
      destItem.checked = true;
      matched++;
    }

    // Recursively process children
    if (destItem.children && matchingSource?.children) {
      destItem.childrenMatched = updateCheckedProperty(
        matchingSource.children,
        destItem.children
      );
    }
  }
  return matched;
}

function checkParentCheckboxes(checkbox) {
  let parentLi = checkbox.closest("li"); // Find the closest <li> of the current checkbox

  while (parentLi) {
    const parentCheckbox = parentLi.querySelector('input[type="checkbox"]'); // Get the checkbox in this parent <li>

    if (parentCheckbox) {
      parentCheckbox.checked = true; // Check the parent checkbox
    }

    // Move to the next parent <li> by traversing up to the parent <ul>
    parentLi = parentLi.parentElement?.closest("li");
  }
}

function setAllChildCheckboxes(checkbox, checked) {
  let parentLi = checkbox.closest("li");
  const checkboxes = parentLi.querySelectorAll('input[type="checkbox"]');
  for (const checkbox of checkboxes) {
    checkbox.checked = checked;
  }
}

// Function to create a tree view of bookmarks with checkboxes
function createBookmarkTree(bookmarks, container, preCheck = false) {
  //debugger
  for (const bookmark of bookmarks) {
    const li = document.createElement("li");

    li.style.alignItems = "center"; // Vertically align items
    li.style.marginBottom = "5px"; // Optional: space between list items
    li.style.outline = "none";
    li.style.listStyleType = "none";
    // Create a checkbox for the folder or bookmark
    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.value = bookmark.url || bookmark.id; // Use URL for bookmarks, ID for folders

    checkbox.style.transform = "scale(1.2)";
    checkbox.style.marginRight = "5px";

    checkbox.checked = bookmark.checked;

    const title = document.createElement("span");
    title.textContent = bookmark.title;
    title.style.fontSize = "14px"; // Increase font size for the title
    title.style.whiteSpace = "normal"; // Allow title to wrap if necessary
    title.style.overflowWrap = "break-word"; // Break long words to prevent overflo

    // If the bookmark is a folder, recursively create children
    if (bookmark.children && bookmark.children.length > 0) {
      checkbox.addEventListener("change", function () {
        if (this.checked) {
          checkParentCheckboxes(this); // Ensure all parent checkboxes are checked

          setAllChildCheckboxes(this, true);
        } else {
          setAllChildCheckboxes(this, false);
        }
      });

      const ul = document.createElement("ul");
      ul.style.marginBottom = "5px";
      ul.style.marginTop = "5px";
      ul.style.display = "none"; // Initially hide the children (collapsed state)
      ul.style.outline = "none";
      ul.style.listStyleType = "none";
      // Create a button for expand/collapse
      const toggleButton = document.createElement("button");
      toggleButton.textContent = "+"; // Initially show as expandable
      toggleButton.style.marginRight = "5px";

      toggleButton.style.background = "none"; // Remove background
      toggleButton.style.border = "none"; // Remove border for a cleaner look
      toggleButton.style.fontSize = "18px"; // Make button text smaller
      toggleButton.style.padding = "0"; // Remove padding to make it more compact
      toggleButton.style.cursor = "pointer"; // Change the cursor to pointer to indicate it's clickable
      toggleButton.style.outline = "none";
      toggleButton.style.alignItems = "center";

      // Toggle the UL visibility when the button is clicked
      toggleButton.addEventListener("click", () => {
        if (ul.style.display === "none") {
          ul.style.display = "block"; // Show children (expand)
          toggleButton.textContent = "-"; // Change to collapse symbol
        } else {
          ul.style.display = "none"; // Hide children (collapse)
          toggleButton.textContent = "+"; // Change to expand symbol
        }
      });
      // Use flexbox to align elements in a row

      li.appendChild(toggleButton); // Append the button to the li
      li.appendChild(checkbox);
      li.appendChild(title);

      createBookmarkTree(bookmark.children, ul, preCheck); // Await recursive call

      li.appendChild(ul); // Append the UL (children list) to the li
    } else {
      checkbox.addEventListener("change", function () {
        if (this.checked) {
          checkParentCheckboxes(this);
        }
      });
      const lockSpan = document.createElement("span");
      lockSpan.innerHTML = "&#128278;";

      title.textContent = "";
      title.innerHTML = `<a href="${bookmark.url}" >${bookmark.title} </a>`;

      li.appendChild(lockSpan);
      li.appendChild(checkbox);
      li.appendChild(title);
    }

    container.appendChild(li);
  }
}

function createBookmarkStructure(bookmarks) {
  const stack = []; // Stack to track parent-child relationships based on indentation
  const result = []; // The final structure to hold the hierarchy of bookmarks

  bookmarks.forEach((bookmark) => {
    // Determine the indentation level (2 spaces per level)
    const indentLevel = (bookmark.title.match(/^ */) || [""])[0].length / 2;
    const actualTitle = bookmark.title.trim(); // Remove leading spaces

    // Create the bookmark object
    const bookmarkObj = {
      title: actualTitle,
      url: bookmark.url || "", // If no URL, set it to empty string
      children: [], // Initialize an empty children array
    };

    // If we are at root level (indentLevel 0), push directly to the result
    if (indentLevel === 0) {
      result.push(bookmarkObj);
    } else {
      // Pop elements from stack until we find the correct parent (matching indent level)
      while (stack.length > indentLevel) {
        stack.pop(); // Move up to the correct parent level
      }

      // Find the parent and push the current bookmark as its child
      const parent = stack[stack.length - 1];
      parent.children.push(bookmarkObj);
    }

    // Push the current bookmark to the stack to be a parent for future bookmarks
    stack.push(bookmarkObj);
  });

  return result;
}
async function deleteElementsWithBookmarkProfile() {
  return new Promise((resolve) => {
    const elements = document.querySelectorAll("[bookmarkProfile]");
    for (const element of elements) {
      element.remove();
    }
    resolve();
  });
}

// Function to render bookmarks for all profiles
async function renderOtherBookmarks(bookmarksData) {
  const container = document.getElementById("other-bookmarks");

  await deleteElementsWithBookmarkProfile();
  const result = await getFromStorage(["profileName"]);

  for (const profile of bookmarksData) {
    if (
      result &&
      result.profileName &&
      result.profileName == profile.profileName
    ) {
      continue;
    }

    const profileSection = document.createElement("div");
    profileSection.style.marginBottom = "20px";
    profileSection.setAttribute("bookmarkProfile", profile.profileName);

    // Create profile header
    const profileHeader = document.createElement("h3");
    profileHeader.textContent = profile.profileName;
    profileHeader.className = "user-list";
    profileSection.appendChild(profileHeader);

    // Create bookmarks container for the profile
    const bookmarksContainer = document.createElement("ul");
    bookmarksContainer.style.paddingLeft = "20px";
    profileSection.appendChild(bookmarksContainer);

    // Render bookmarks for the profile
    createBookmarkTree(profile.bookmarks, bookmarksContainer);

    // Append profile section to the main container
    container.appendChild(profileSection);
  }
}


function getSelectedBookmarks(root) {
  const checkboxes = getImmediateCheckboxChildren(root);

  function buildBookmarkTree(checkbox) {
    const title =
      (checkbox.nextSibling.innerText || checkbox.nextSibling.textContent) + "";
    const url = checkbox.value.startsWith("http") ? checkbox.value : null;

    // Check if this bookmark has children
    const children = [];
    const parentLi = checkbox.closest("li");

    // Look for nested <ul> (children) inside the current parent
    const childList = parentLi.querySelector("ul"); // Only check if there's a <ul> (child list)

    if (childList) {
      // Use the utility function to find immediate checkbox children
      const childCheckboxes = getImmediateCheckboxChildren(childList);
      for (const childCheckbox of childCheckboxes) {
        if (childCheckbox.checked) {
          children.push(buildBookmarkTree(childCheckbox));
        }
      }
    }

    return { title, url, children: children.length ? children : null };
  }

  // Map over all checked checkboxes and build the hierarchy
  return Array.from(checkboxes).map((checkbox) => {
    const bktree = buildBookmarkTree(checkbox);
    return bktree;
  });
}

async function createBookmarksFromProfiles() {
  // Get all profile divs with the "bookmarkProfile" attribute
  const profileDivs = document.querySelectorAll("div[bookmarkProfile]");

  for (const profileDiv of profileDivs) {
    let firstUl;
    let firstLi;

    firstUl = profileDiv.querySelector("ul"); // Find the first <ul> under the profile div
    if (firstUl) {
      firstLi = firstUl.querySelector("li"); // Find the first <li> under the first <ul>
      if (firstLi) {
        console.log(firstLi); // This is the first <li> under the first <ul> (grandchild)
      }
    }

    // Get the profile name from the 'bookmarkProfile' attribute
    const profileName = profileDiv.getAttribute("bookmarkProfile");

    // Get the selected bookmarks for this profile
    const selectedBookmarks = getSelectedBookmarks(firstUl);

    if (!selectedBookmarks[0].children) continue;

    // Now let's create a top-level bookmark using the profile name
    const profileBookmark = {
      title: profileName, // Profile name as the title
      url: "", // No URL for the profile itself
      children: selectedBookmarks[0].children, // The selected bookmarks will be children
    };

    // Now add this profile bookmark to the user's bookmark bar
    await addBookmarkToBookmarkBar(profileBookmark);
  }
}

async function addBookmarkToBookmarkBar(bookmark) {
  // Check if a profile folder already exists with the same title (profile name)
  const allMatchingFolders = await new Promise((resolve) =>
    chrome.bookmarks.search({ title: bookmark.title }, resolve)
  );

  // Find a folder with the correct parentId
  const existingFolder = allMatchingFolders.find(
    (folder) => folder.parentId === "1"
  );

  if (!existingFolder) {
    // Create the root folder for the profile if it doesn't already exist
    chrome.bookmarks.create(
      {
        parentId: "1", // This is the ID for the bookmark bar
        title: bookmark.title, // Profile name becomes the folder's title
      },
      async function (profileFolder) {
        // Now that the profile folder is created, add its children (selected bookmarks)
        await addBookmarksToFolder(profileFolder.id, bookmark.children);
      }
    );
  } else {
    console.log(`Profile folder "${bookmark.title}" already exists.`);
    // Optionally, add children under the existing folder
   // await deleteAllBookmarksInFolder(existingFolder.id)
    await addBookmarksToFolder(existingFolder.id, bookmark.children);
  }
}
function deleteAllBookmarksInFolder(folderId) {
  return new Promise((resolve, reject) => {
    // Get all children within the folder
    chrome.bookmarks.getChildren(folderId, (children) => {
      if (chrome.runtime.lastError) {
        reject(`Error fetching bookmarks: ${chrome.runtime.lastError.message}`);
        return;
      }

      if (!children || children.length === 0) {
        resolve("Folder is already empty");
        return;
      }

      // Track deletion promises
      const deletionPromises = [];

      for (const child of children) {
        const deletePromise = new Promise((res, rej) => {
          chrome.bookmarks.remove(child.id, () => {
            if (chrome.runtime.lastError) {
              rej(`Error deleting bookmark: ${chrome.runtime.lastError.message}`);
            } else {
              res();
            }
          });
        });

        deletionPromises.push(deletePromise);
      }

      // Wait for all deletions to complete
      Promise.all(deletionPromises)
        .then(() => resolve("All bookmarks deleted successfully"))
        .catch((error) => reject(error));
    });
  });
}
async function addBookmarksToFolder(parentId, bookmarks) {
  // debugger
  for (const bookmark of bookmarks) {
    if (bookmark.url) {
      // Check if the bookmark already exists in the folder
      const allMatchingBookmarks = await new Promise((resolve) =>
        chrome.bookmarks.search({ url: bookmark.url }, resolve)
      );

      const existingBookmark = allMatchingBookmarks.find(
        (b) => b.parentId === parentId
      );

      if (!existingBookmark) {
        // Create a bookmark if it doesn't already exist
        chrome.bookmarks.create(
          {
            parentId: parentId, // Parent folder ID
            title: bookmark.title, // Bookmark title
            url: bookmark.url, // Bookmark URL
          },
          function (newBookmark) {
            console.log("Created bookmark:", newBookmark);
          }
        );
      } else {
        console.log(`Bookmark "${bookmark.title}" already exists.`);
      }
    } else if (bookmark.children && bookmark.children.length > 0) {
      // If it's a folder (no URL, has children), check if a folder with the same title exists
      const allMatchingFolders = await new Promise((resolve) =>
        chrome.bookmarks.search({ title: bookmark.title }, resolve)
      );

      const existingFolder = allMatchingFolders.find(
        (folder) => folder.parentId === parentId
      );

      if (!existingFolder) {
        chrome.bookmarks.create(
          {
            parentId: parentId,
            title: bookmark.title, // Folder title
          },
          function (folder) {
            // Recursively add the children of the folder
            addBookmarksToFolder(folder.id, bookmark.children);
          }
        );
      } else {
        console.log(`Folder "${bookmark.title}" already exists.`);
        // Recursively add children to the existing folder
        addBookmarksToFolder(existingFolder.id, bookmark.children);
      }
    }
  }
}

// Save the profile name when the user submits it
document
  .getElementById("profile-name")
  .addEventListener("change", async (event) => {
    const profileName = event.target.value.trim();
    if (profileName) {
      await setToStorage({ profileName: profileName });
    }
  });
function getFromStorage(keys) {
  return new Promise((resolve, reject) => {
    chrome.storage.local.get(keys, (result) => {
      if (chrome.runtime.lastError) {
        reject(chrome.runtime.lastError);
      } else {
        resolve(result);
      }
    });
  });
}

function setToStorage(data) {
  return new Promise((resolve, reject) => {
    chrome.storage.local.set(data, () => {
      if (chrome.runtime.lastError) {
        reject(chrome.runtime.lastError);
      } else {
        resolve();
      }
    });
  });
}
function sendMessageToRuntime(message) {
  return new Promise((resolve, reject) => {
    chrome.runtime.sendMessage(message, (response) => {
      if (chrome.runtime.lastError) {
        reject(chrome.runtime.lastError);
      } else {
        resolve(response);
      }
    });
  });
}

async function testOtherBookmark() {
  const bookmarks1 = [
    { title: "Bookmarks bar", url: "" },
    { title: "  Tutorials", url: "" },
    { title: "    Architecture", url: "" },
    {
      title: "      How to Interview a Software Architect",
      url: "http://example.com/architect",
    },
    {
      title: "      Microservices vs SOA",
      url: "http://example.com/microservices",
    },
    { title: "  Tech Domains", url: "" },
    { title: "    NodeJS", url: "" },
    {
      title: "      NodeJS Interview Questions.md · GitHub",
      url: "http://example.com/nodejs",
    },
    { title: "    JavaScript", url: "http://example.com/js" },
    { title: "    ReactJS", url: "http://example.com/react" },
    { title: "    React Native", url: "http://example.com/react-native" },
  ];

  const bookmarks2 = [
    { title: "Bookmarks bar", url: "" },
    { title: "  Tutorials", url: "" },

    {
      title: "      Microservices vs SOA",
      url: "http://example.com/microservices",
    },
    { title: "  Tech Domains", url: "" },
    { title: "    NodeJS", url: "" },
    {
      title: "      NodeJS Interview Questions.md · GitHub",
      url: "http://example.com/nodejs",
    },
    { title: "    JavaScript", url: "http://example.com/js" },
  ];

  const bookmarksData = [
    {
      profileName: "Anil 1",
      bookmarks: createBookmarkStructure(bookmarks1),
    },
    {
      profileName: "Anil 2",
      bookmarks: createBookmarkStructure(bookmarks2),
    },
  ];
}
