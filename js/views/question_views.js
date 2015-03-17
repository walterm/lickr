Lickr.QuestionView = Ember.View.extend({
    templateName: 'question',
    didInsertElement: function () {
        this.$('img').click(function(evt){
            // this maps to the image in here
            $('.selected').removeClass('selected');
            // question: why can't i use this.$().addClass()?
            $(this).addClass('selected');
        });
    }
});