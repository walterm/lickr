Lickr.ApplicationController = Ember.Controller.extend({
    confDict: {},
    actions: {
        addColor: function (hex_code) {
            var dict = this.get("confDict"),
                keys = Object.keys(dict);

            if(_.find(keys, function(key){return key === hex_code}) !== undefined){
                dict[key] *= 1.5
            } else {
                dict[key] = 0.5
            }
        },
        getTopColors: function(confDict){
            var colors = Object.keys(this.get("confDict"));
            colors.sort(function(a, b){
                return confDict[b] - confDict[a]; // descending order
            });

            colors = colors.slice(0,4); // top 4
            var d = {};
            _.each(colors, function(color){
                d[color] = confDict[color];
            });
            return d;
        }
    }
});

Lickr.QuestionController = Ember.Controller.extend({
    needs: ['application'],
    confDict: Ember.computed.alias('controllers.application.confDict'),
    currentImgs: [],
    actions: {
        test: function() {
            // var current = this.get('model').get('id');
            // current = parseInt(current,10) + 1;

            // if(current > this.get('numModels')){
            //     this.transitionToRoute('results');
            // } else this.transitionToRoute('question');
        },
        addCurrentImg: function(img_obj){
            this.get('currentImgs').push(img_obj);
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

            this.transitionToRoute('question');
        }
    }
});