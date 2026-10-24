// Adds a "Website" menu to the Google Sheet with a "Publish now" button.
// Paste this into Extensions > Apps Script in the Sheet (see README).
const REPO = 'Stamp00/Cassandra_porfolio';
const WORKFLOW = 'build.yml';

function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu('Website')
    .addItem('Publish now', 'publishNow')
    .addSeparator()
    .addItem('Set GitHub key (one time)', 'setKey')
    .addToUi();
}

function setKey() {
  const ui = SpreadsheetApp.getUi();
  const r = ui.prompt('GitHub key', 'Paste the GitHub key (starts with github_pat_):', ui.ButtonSet.OK_CANCEL);
  if (r.getSelectedButton() !== ui.Button.OK) return;
  PropertiesService.getDocumentProperties().setProperty('GITHUB_TOKEN', r.getResponseText().trim());
  ui.alert('Saved. You can now use Website > Publish now.');
}

function publishNow() {
  const ui = SpreadsheetApp.getUi();
  const token = PropertiesService.getDocumentProperties().getProperty('GITHUB_TOKEN');
  if (!token) {
    ui.alert('Add the GitHub key first: Website > Set GitHub key.');
    return;
  }
  SpreadsheetApp.flush();
  const res = UrlFetchApp.fetch(
    'https://api.github.com/repos/' + REPO + '/actions/workflows/' + WORKFLOW + '/dispatches', {
      method: 'post',
      contentType: 'application/json',
      headers: { Authorization: 'Bearer ' + token, Accept: 'application/vnd.github+json' },
      payload: JSON.stringify({ ref: 'main' }),
      muteHttpExceptions: true,
    });
  if (res.getResponseCode() === 204) {
    SpreadsheetApp.getActive().toast('The website will update in about 2 minutes.', 'Publishing', 8);
  } else {
    ui.alert('Could not publish (' + res.getResponseCode() + '). The GitHub key may be wrong or expired.\n\n' + res.getContentText().slice(0, 300));
  }
}
