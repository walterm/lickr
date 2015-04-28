Lickr.ApplicationController = Ember.Controller.extend({
    confDict: {}
});

Lickr.QuestionController = Ember.Controller.extend({
    needs: ['application'],
    confDict: Ember.computed.alias('controllers.application.confDict'),

    actions: {
        test: function() {
            // var current = this.get('model').get('id');
            // current = parseInt(current,10) + 1;

            // if(current > this.get('numModels')){
            //     this.transitionToRoute('results');
            // } else this.transitionToRoute('question');
        },
        addImage: function(img) {
            this.get('selectedColors').push(img);
        }
    }
});

Lickr.ResultsController = Ember.ObjectController.extend({
    needs: ['application'],
    confDict: Ember.computed.alias('controllers.application.confDict'),
});

Lickr.StartController = Ember.Controller.extend({
    needs: ['application'],
    confDict: Ember.computed.alias('controllers.application.confDict'),
    actions: {
        favorite: function (color) {
            var colorToCode = {
                'Red': 'ff0000',
                'Orange': 'ffa500',
                'Yellow': 'ffff00',
                'Green': '008000',
                'Blue': '0000ff',
                'Purple': '800080'
            };
            var fave = $(".color-selected");
            this.get('confDict')[colorToCode[$(fave).find(".code").html()]] = 0.5;
            console.log(this.get('confDict'));
        }
    }
});