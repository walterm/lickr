Lickr.Router.map(function() {
    this.resource('question', {path: '/q/:q_id'});
    this.resource('results', {path: '/results'});
});

Lickr.QuestionRoute = Ember.Route.extend({
    setupController: function(controller, model) {     
        controller.set('model', model);
        controller.set('numModels', 11); // TODO: get the RESTAdapter to count the number of questions
    },
    model: function (params) {
        return this.store.find('question', params.q_id);
    }
});
