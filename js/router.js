Lickr.Router.map(function() {
    this.resource('questions', {path: "/"});
});

Lickr.QuestionsRoute = Ember.Route.extend({
    model: function () {
        return this.store.find('question');
    }
});