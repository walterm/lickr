Lickr.ApplicationController = Ember.Controller.extend({
    confDict: {},
    currentQuestion: 1,
    seenImgs: []
});

var getTopColors = function(confDict){
    var colors = Object.keys(confDict);
    colors.sort(function(a, b){
        return confDict[b] - confDict[a]; // descending order
    });

    colors = colors.slice(0,4); // top 4
    var d = {};
    _.each(colors, function(color){
        d[color] = confDict[color];
    });
    return d;
};

Lickr.QuestionController = Ember.Controller.extend({
    needs: ['application'],
    confDict: Ember.computed.alias('controllers.application.confDict'),
    currentQuestion: Ember.computed.alias('controllers.application.currentQuestion'),
    seenImgs: Ember.computed.alias('controllers.application.seenImgs'),
    currentImgs: [],
    selectedImg: undefined,
    nextQuestion: false,
    actions: {
        addImg: function(img_obj){
            this.get('currentImgs').push(img_obj);

        },
        findImg: function(img_id){
            var imgs = this.get('currentImgs');
            this.get('seenImgs').push(img_id);
            this.set('selectedImg', _.find(imgs, function(img){ return img['_id'] == img_id; }))
        },
        updateConfDict: function(colors) {
            var confDict = this.get('confDict');
            var updated = {},
                currentColors = Object.keys(confDict);
            _.each(currentColors, function(color){
                updated[color] = false;
            });

            _.each(colors, function(color){
                if(currentColors.indexOf(color) !== -1){
                    updated[color] = true
                    confDict[color] *= 1.5
                } else {
                    confDict[color] = 0.5;
                }
            });



            var not_updated = _.filter(Object.keys(updated), function(color){ return ! updated[color];});
            _.each(not_updated, function(color){
                confDict[color] *= 0.5;
            });

            var factor = _.values(confDict).reduce(function(a,b){return a+b}, 0);

            _.each(_.keys(confDict), function(k){ confDict[k] /= factor;});
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
        advance: function() {
            // update confDict
            var img_id = $('.selected').attr('img_id');
            // var selectedImage = findImg(img_id);
            this.send('findImg', img_id);
            var img_colors = this.get('selectedImg')['top_colors'];
            this.send('updateConfDict', img_colors);
            // if we're confident redirect to results
            if(this.get('currentQuestion') < 15) {
                var next = this.get('currentQuestion') + 1;
                this.set('currentQuestion', next);
                this.transitionToRoute('question', next);
            } else {
                this.transitionToRoute('results');
            }
            // else continue to next question
        }
    }
});

Lickr.ResultsController = Ember.ObjectController.extend({
    needs: ['application'],
    confDict: Ember.computed.alias('controllers.application.confDict'),
    currentQuestion: Ember.computed.alias('controllers.application.currentQuestion'),
    seenImgs: Ember.computed.alias('controllers.application.seenImgs'),
    actions: {
        restart: function () {
            this.set('confDict', {});
            this.set('currentQuestion', 1);
            this.set('seenImgs', []);
            this.transitionToRoute('start');
        }
    }
});

Lickr.InfoController = Ember.Controller.extend({
    actions: {
        start: function() {
            this.transitionToRoute('start');
        }
    }
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

            this.transitionToRoute('question', 1);
        }
    }
});