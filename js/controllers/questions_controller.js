Lickr.ApplicationController = Ember.Controller.extend({
    selectedImages: []
});

Lickr.QuestionController = Ember.ObjectController.extend({
    needs: ['application'],
    selectedImages: Ember.computed.alias('controllers.application.selectedImages'),
    actions: {
        test: function() {
            var current = this.get('model').get('id');
            current = parseInt(current,10) + 1;

            if(current > this.get('numModels')){
                this.transitionToRoute('results');
            } else this.transitionToRoute('question',current);
        },
        addImage: function(img) {
            this.get('selectedImages').push(img);
        }
    }
});

Lickr.ResultsController = Ember.ObjectController.extend({
    needs: ['application'],
    selectedImages: Ember.computed.alias('controllers.application.selectedImages')
});