Lickr.Router.map(function() {
    this.resource('question', {path: '/q'});
    this.resource('results', {path: '/results'});
    this.resource('start', {path: '/'});
});

Lickr.QuestionRoute = Ember.Route.extend({});
