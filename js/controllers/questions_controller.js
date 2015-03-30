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
                // TODO: post to Flask to do image processing
                $.ajax({
                    type: 'POST',
                    url: 'http://127.0.0.1:8000/process_imgs',
                    data: {'imgs': ['test', 'val']}
                }).success(function(data){
                    console.log(data);
                });

                this.transitionToRoute('results');
            } else this.transitionToRoute('question',current);
        },
        addImage: function(img) {
            this.get('selectedImages').push(img);
        }
    }
});