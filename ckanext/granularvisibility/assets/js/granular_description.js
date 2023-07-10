
function updateHelpText() {
    var selectElement = $('#field-visibility');
    var selectedOption = selectElement.find('option:selected');
    var helpBlock = $('#viz-description');
    helpBlock.text(selectedOption.data('description'));
}
// Call updateHelpText() to handle the initial render of the selected option
updateHelpText();

$('#field-visibility').on('change', updateHelpText);

