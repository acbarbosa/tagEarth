var Tag = function(name, selected) {
  this.name = name;
  this.selected = ko.observable(selected);
};
Tag.prototype.toggleSelected = function() {
  this.selected( !this.selected() );
};

var tags = [
   new Tag("Cloudy", false), 
   new Tag("Desert", false),
   new Tag("fire", false),
   new Tag("fog", false),
   new Tag("geiser", false),
   new Tag("glacier", false),
   new Tag("hill", false),
   new Tag("ice", false),
   new Tag("iceberg", false),
   new Tag("island", false),
   new Tag("lagoon", false),
   new Tag("lake", false),
   new Tag("mountains", false),
   new Tag("ravine", false),
   new Tag("river", false),
   new Tag("sea", false),
   new Tag("urban area", false),
   new Tag("vegetation", false),
   new Tag("volcano", false)
];

var TagViewModel = function(tags) {
  this.tags = ko.observableArray(tags);
};
TagViewModel.prototype.submissionData = ko.computed (function() {
  var selectedTags = _.filter(this.tags, function(tag) { return tag.selected(); });
  return { tags: selectedTags };
});


ko.applyBindings( new TagViewModel(tags) );

