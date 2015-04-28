Lickr.Router.map(function() {
    this.resource('question', {path: '/q'});
    this.resource('results', {path: '/results'});
    this.resource('start', {path: '/'});
});

Lickr.QuestionRoute = Ember.Route.extend({
    setupController: function(controller, model) {     
        controller.set('model', model);
        controller.set('numModels', 11);
    },
    model: function (params) {
        return this.store.find('question', params.q_id);
    }
});
