define("ace/mode/gpss", function(require, exports, module) {
  "use strict";
  
  const oop = require("ace/lib/oop");
  const TextMode = require("ace/mode/text").Mode;
  const GpssHighlightRules = require("ace/mode/gpss_highlight_rules").GpssHighlightRules;
  
  const Mode = function() {
    this.HighlightRules = GpssHighlightRules;
  };
  oop.inherits(Mode, TextMode);
  exports.Mode = Mode;
});

define("ace/mode/gpss_highlight_rules", function(require, exports, module) {
  "use strict";
  
  const oop = require("ace/lib/oop");
  const TextHighlightRules = require("ace/mode/text_highlight_rules").TextHighlightRules;
  
  const GpssHighlightRules = function () {
    this.$rules = {
      start: [
        {
          token: "keyword",
          regex: /(?<!\S)(?:CLEAR|END|RESET|SIMULATE|START|STORAGE|ADVANCE|DEPART|ENTER|GENERATE|LEAVE|QUEUE|RELEASE|SEIZE|TERMINATE|TRANSFER)(?![^\s;*])/,
          caseInsensitive: true,
        },
        {
          token: "constant",
          regex: /(?<![^\s,])(?:0?\.)?[0-9]+(?![^\s,;*])/,
        },
        {
          token: "comment",
          regex: /[;*].*$/,
        },
      ],
    };
    
    this.normalizeRules();
  };
  GpssHighlightRules.metaData = {
    name: "GPSS",
    fileTypes: [
      "gps",
      "gpss",
    ],
  };
  oop.inherits(GpssHighlightRules, TextHighlightRules);
  exports.GpssHighlightRules = GpssHighlightRules;
});
