Lickr.QuestionView = Ember.View.extend({
    templateName: 'question',
    didInsertElement: function () {
        this.$('img').click(function(evt){
            $('.selected').removeClass('selected');
            $('#next').removeAttr('disabled');
            $(this).addClass('selected');
        });
    }
});