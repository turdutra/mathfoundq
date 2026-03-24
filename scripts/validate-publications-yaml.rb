require "yaml"

path = File.expand_path("../mfq/content/english/publications/publications.yaml", __dir__)
required_keys = %w[title link authors published_in date].freeze

data = YAML.safe_load(File.read(path), permitted_classes: [], aliases: false)

unless data.is_a?(Hash) && data["publications"].is_a?(Array)
  warn "Expected a top-level 'publications' list in #{path}"
  exit 1
end

errors = []

data["publications"].each_with_index do |publication, index|
  unless publication.is_a?(Hash)
    errors << "Entry #{index + 1} is not a mapping"
    next
  end

  missing = required_keys.select do |key|
    value = publication[key]
    value.nil? || (value.respond_to?(:empty?) && value.empty?)
  end

  if missing.any?
    errors << "Entry #{index + 1} is missing: #{missing.join(', ')}"
  end

  authors = publication["authors"]
  if authors && (authors.is_a?(Array) == false || authors.empty?)
    errors << "Entry #{index + 1} has an invalid authors list"
    next
  end

  authors.each_with_index do |author, author_index|
    unless author.is_a?(Hash)
      errors << "Entry #{index + 1} author #{author_index + 1} must be a mapping"
      next
    end

    name = author["name"]
    page = author["page"]

    if !name.is_a?(String) || name.strip.empty?
      errors << "Entry #{index + 1} author #{author_index + 1} is missing a valid name"
    end

    if !page.nil? && (!page.is_a?(String) || page.strip.empty?)
      errors << "Entry #{index + 1} author #{author_index + 1} has an invalid page slug"
    end
  end
end

if errors.empty?
  puts "Validated #{data['publications'].length} publications in #{path}"
  exit 0
end

errors.each do |error|
  warn error
end
exit 1
