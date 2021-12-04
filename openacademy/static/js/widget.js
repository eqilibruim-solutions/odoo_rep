odoo.define('hello_world_widget', (require) => {
    "use strict";

    let AbstractField = require('web.AbstractField');
    let fieldRegistry = require('web.field_registry');

    let helloWorldField = AbstractField.extend({
        className: 'o_hello_world';
        tagName: 'span';
        supportedFieldTypes: ['html', 'char']

        events: {
        }

        init: function() {
        }
    })
})


