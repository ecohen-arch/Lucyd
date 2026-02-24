// Click the note_add button for the target category to create a new article in it
// categoryIndex: 0=Warranty, 1=Product, 2=Orders
var categoryIndex = CATEGORY_INDEX;

var noteAddBtns = Array.from(document.querySelectorAll('button')).filter(function(b) {
    return b.textContent.trim() === 'note_add';
});

if (noteAddBtns[categoryIndex]) {
    noteAddBtns[categoryIndex].click();
    "clicked note_add for category " + categoryIndex;
} else {
    "note_add button not found for index " + categoryIndex;
}
