# Sceptre CloudFront invalidation hook

Provides hook to trigger invalidation on CloudFront distribution.

## Usage

In your config file, add the hook as follows:

```yaml
hooks:
  hook_point:
    - !cloudfront_invalidate distributionIdSpecifier paths...
```

`distributionIdSpecifier` can be either `Resources.MyResourceName` or `Outputs.MyOutputName`

Multiple paths can be specified in a single request.
