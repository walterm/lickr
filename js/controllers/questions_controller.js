Lickr.ApplicationController = Ember.Controller.extend({
    confDict: {}
});

Lickr.QuestionController = Ember.Controller.extend({
    needs: ['application'],
    confDict: Ember.computed.alias('controllers.application.confDict'),
    currentImgs: [],
    actions: {
        addCurrentImg: function(img_obj){
            this.get('currentImgs').push(img_obj);
        },
        findImg: function(img_id){
            var imgs = this.get('currentImgs');
            return _.find(imgs, function(img){ return img['_id'] == img_id; }); // should for sure be there
        },
        addColor: function (hex_code) {
            var dict = this.get("confDict"),
                keys = Object.keys(dict);

            if(_.find(keys, function(key){return key === hex_code}) !== undefined){
                dict[key] *= 1.5
            } else {
                dict[key] = 0.5
            }
        },

        advance: {
            
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