Lickr.Router.map(function() {
    this.resource('question', {path: '/q/:id'});
    this.resource('results', {path: '/results'});
    this.resource('start', {path: '/favorite'});
    this.resource('info', {path: '/'});
});

Lickr.QuestionRoute = Ember.Route.extend({});
