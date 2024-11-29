const GOOGLE_SHEET_ID = "1iSFI29fTLPyVMOq25CJEsacxsVWg0OWocIvIIhpmJFE"; // Replace with your Google Sheet ID
chrome.runtime.onInstalled.addListener(() => {
    console.log("Bookmark Extension Installed");
  });
  chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === "shareBookmarks") {
      authenticate((token) => {
        updateSheet(token, message.profileName, message.bookmarks);
      });
    }
  });

  // Function to authenticate the user with Google
  function authenticate(callback) {
    chrome.identity.getAuthToken({ interactive: true }, (token) => {
      if (chrome.runtime.lastError || !token) {
        console.error("Error obtaining auth token: ", chrome.runtime.lastError);
        return;
      }
      callback(token); // Pass the token to the callback
    });
  }

  async function getSheetIdByName(spreadsheetId, token, sheetName) {
    const response = await fetch(`https://sheets.googleapis.com/v4/spreadsheets/${spreadsheetId}`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        }
    });

    if (!response.ok) {
        throw new Error(`Failed to fetch spreadsheet metadata: ${response.statusText}`);
    }

    const data = await response.json();

    for (const sheet of data.sheets){
        if (sheet.properties.title == sheetName)
        {
            return sheet.properties.sheetId;
        }
    }
       
    return -1
}
async function clearSheet(spreadsheetId,sheetId, token) {
    
    const clearRequests = [
        {
          updateCells: {
            range: {
              sheetId: sheetId, // Replace this with your specific sheetId
            },
            fields: "*", // Clear everything (values, formatting, etc.)
          },
        },
      ];
      // Send the request to clear the sheet
      const clear_reponse = await fetch(
        `https://sheets.googleapis.com/v4/spreadsheets/${spreadsheetId}:batchUpdate`,
        {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ requests: clearRequests }),
        }
      );
      // Wait for the response to be converted to JSON
      const clear_data = await clear_reponse.json();
  
      // Log success message with data
      console.log("Sheet clearly successfully:", clear_data);
}

async function clearSheetValues(spreadsheetId, token, sheetName) {
  // const sheetId = await getSheetIdByName(spreadsheetId, token, sheetName); // Fetch the sheetId
  const range = `${sheetName}!A:Z`; // Adjust range as needed (e.g., A:Z clears all rows/columns in A-Z)
  const url = `https://sheets.googleapis.com/v4/spreadsheets/${spreadsheetId}/values/${range}:clear`;

  const response = await fetch(url, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    },
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(`Failed to clear values: ${error.error.message}`);
  }

  return response.json();
}

function flattenBookmarks(rows, bookmarks, level = 0) {
  try {
    for (const bookmark of bookmarks) {
      // Add the current bookmark or folder to the rows
      const indentation = " ".repeat(level * 2); // Indent based on level
      rows.push([`${indentation}${bookmark.title}`, bookmark.url || ""]);

      // If the bookmark has children, recursively process them
      if (bookmark.children && bookmark.children.length > 0) {
        flattenBookmarks(rows, bookmark.children, level + 1);
      }
    }
  } catch (e) {}

  // return rows;
}
// Function to send data to Google Sheets
async function updateSheet(token, profileName, bookmarks) {
  const spreadsheetId = GOOGLE_SHEET_ID; // Replace with your actual Google Sheet ID
  profileName = await getUserEmail(token);
  const range = `${profileName}!A1:B`; // Specify the sheet and range

  const sheetId = await createSheetIfNotExists(spreadsheetId, profileName, token);
  await clearSheetValues(spreadsheetId, token, profileName);
  const rows = [];
  // Flatten the bookmarks hierarchy
  flattenBookmarks(rows, bookmarks);
  const values = rows;

  const body = {
    range: range,
    majorDimension: "ROWS",
    values: values,
  };

  // Send PUT request to Google Sheets API
  const response = await fetch(
    `https://sheets.googleapis.com/v4/spreadsheets/${spreadsheetId}/values/${range}?valueInputOption=RAW`,
    {
      method: "PUT",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body),
    }
  );

  // Wait for the response to be converted to JSON
  const data = await response.json();

  // Log success message with data
  console.log("Sheet updated successfully:", data);
}


  
  // Function to create a sheet in Google Sheets if it doesn't exist
// Async function to create a sheet if it doesn't exist
async function createSheetIfNotExists(spreadsheetId, sheetName, token) {
    try {

      const sheetId =  await getSheetIdByName(spreadsheetId, token, sheetName)
      // Step 2: If sheet does not exist, create it
      if (sheetId == -1) {
        console.log(`Sheet "${sheetName}" does not exist. Creating it...`);

        const requests = [
          {
            addSheet: {
              properties: {
                title: sheetName,
              },
            },
          },
        ];

        // Step 3: Make a request to add the new sheet
        const createResponse = await fetch(
          `https://sheets.googleapis.com/v4/spreadsheets/${spreadsheetId}:batchUpdate`,
          {
            method: "POST",
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ requests }),
          }
        );

        const createData = await createResponse.json();
        console.log(`Sheet "${sheetName}" created successfully.`);
        return createData; // Return the result of the create sheet operation
      } else {
        console.log(`Sheet "${sheetName}" already exists.`);
        return null; // Return null if the sheet exists
      }
    } catch (error) {
      console.error('Error in createSheetIfNotExists:', error);
      throw error;  // Rethrow the error to propagate it
    }
  }
  
  // I am not using this 
  async function getUserEmail(token) {
    try {
      const response = await fetch('https://www.googleapis.com/oauth2/v3/userinfo', {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
        }
      });
      const data = await response.json();
  
      if (data.email) {
        console.log('User email:', data.email);
        return data.email;  // Return the user's email
      } else {
        throw new Error('Email not found');
      }
    } catch (error) {
      console.error('Error retrieving email:', error);
      throw error;
    }
  }
  // I am not using this 
  async function addEmailToSheetPermissions(sheetId, email, token) {
    try {
      const response = await fetch(`https://www.googleapis.com/drive/v3/files/${sheetId}/permissions`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          type: 'user',
          role: 'writer',  // Can be 'reader', 'writer', or 'owner'
          emailAddress: email,
        })
      });
  
      const data = await response.json();
      console.log('Permission added:', data);
      return data;
    } catch (error) {
      console.error('Error adding permission:', error);
      throw error;
    }
  }
  // I am not using this 
  async function shareSheetWithUser(sheetId, token) {
    try {
      // Get the user's email address
      const email = await getUserEmail(token);
  
      if (email) {
        // Add the email to the sheet's permissions
        await addEmailToSheetPermissions(sheetId, email, token);
        console.log('Successfully shared the sheet with the user.');
      } else {
        console.error('Could not retrieve the email address.');
      }
    } catch (error) {
      console.error('Error sharing sheet:', error);
    }
  }
  
  