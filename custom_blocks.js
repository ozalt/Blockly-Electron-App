// custom_blocks.js
Blockly.Blocks['fetch_db'] = {
    init() {
      this.appendDummyInput()
          .appendField("Fetch from DB")
          .appendField(new Blockly.FieldTextInput("SELECT * FROM test_table"), "QUERY");
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setColour(160);
    }
  };