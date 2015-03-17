Lickr.QuestionController = Ember.ObjectController.extend({

    actions: {
        test: function() {
            var current = this.get('model').get('id');
            current = parseInt(current,10) + 1;
            if(current > this.get('numModels')){
                this.transitionToRoute('results');
            } else this.transitionToRoute('question',current);
        }
    }
});