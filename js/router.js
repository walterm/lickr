Lickr.Router.map(function() {
    this.resource('question', {path: '/q/:q_id'});
});

Lickr.QuestionRoute = Ember.Route.extend({
    model: function (params) {
        return this.store.find('question', params.q_id);
    }
});