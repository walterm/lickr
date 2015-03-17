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

Lickr.ResultsView = Ember.View.extend({
    templateName: 'results',
    didInsertElement: function (){
        this.$('.color').each(function(index, div){
            var color = '#'+Math.floor(Math.random()*16777215).toString(16);
            $(div).css('background', color);
        });
    }
});