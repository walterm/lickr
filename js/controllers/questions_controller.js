Lickr.QuestionController = Ember.ObjectController.extend({
    actions: {
        test: function() {
            var current = this.get('model').get('id');
            current = parseInt(current,10) + 1;
            console.log(current);
            
        }
    }
});