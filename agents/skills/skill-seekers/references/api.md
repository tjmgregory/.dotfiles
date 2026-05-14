# Skill-Seekers-Docs - Api

**Pages:** 2

---

## Use Cases | Skill Seekers Docs

**URL:** https://skillseekersweb.com/docs/about/use-cases

**Contents:**
- Documentation
  - About
  - Getting Started
  - Tutorials
  - Manual
    - Scraping
    - Enhancement
    - MCP
    - Platforms
    - Advanced

Skill Seekers solves real problems for developers, teams, and organizations. Here are common scenarios where it excels.

Problem: You’re learning a new framework (React, Vue, Django, FastAPI) and constantly need to reference documentation.

Solution: Create a comprehensive skill once, use it forever.

Result: Claude understands React hooks, components, routing, state management, and best practices. Ask questions, get code examples, debug issues - all context-aware.

Time Saved: 5-10 minutes per conversation × 20 conversations/week = 2+ hours/week

Problem: Your team has internal tools, frameworks, or APIs with documentation scattered across Confluence, GitHub, and Google Docs.

Solution: Unify all sources into a single AI skill.

Result: New team members onboard 3x faster. Everyone has consistent, up-to-date knowledge.

ROI: $50K+ saved in onboarding time for 10-person team

Problem: You joined a new project with 100K+ lines of code and need to understand the architecture, patterns, and workflows quickly.

Solution: Use C3.x codebase analysis for automated insights.

Time Saved: 2-3 weeks of manual code review → 1 hour automated analysis

Problem: You’re writing developer documentation and need examples, best practices, and troubleshooting content.

Solution: Generate comprehensive guides from existing test code.

Result: Documentation completeness goes from 40% → 95%

Problem: Teaching students about modern frameworks requires constantly updated reference materials.

Solution: Create skills for popular frameworks and keep them updated.

Distribution: Share packaged skills (markdown format) with students.

Benefit: Students get consistent, comprehensive reference. Instructors save 10+ hours/semester on material updates.

Problem: You’re researching a complex topic and need to aggregate information from multiple sources (papers, docs, repos).

Solution: Create multi-source skill combining all resources.

Example: AI/ML Research Skill

Result: Comprehensive knowledge base for literature review, implementation guidance, and comparative analysis.

Problem: Repetitive tasks like “update skill when docs change” waste time.

Solution: CI/CD integration with automatic skill updates.

Result: Skills automatically stay up-to-date with framework releases.

Time Savings per Developer:

At $100/hour: $7,100/year savings per developer

For 10-developer team: $71,000/year ROI

**Examples:**

Example 1 (go):
```go
# Create React skill with docs + GitHub examples
skill-seekers scrape --config configs/react.json
skill-seekers enhance output/react/
skill-seekers package output/react/ --upload
```

Example 2 (markdown):
```markdown
# Combine internal docs + GitHub + PDFs
skill-seekers unified --config configs/internal-platform.json
```

Example 3 (json):
```json
{
  "name": "company-platform",
  "sources": [
    {
      "type": "documentation",
      "base_url": "https://internal-docs.company.com/",
      "max_pages": 500
    },
    {
      "type": "github",
      "repository": "company/platform",
      "local_repo_path": "/path/to/platform",
      "include_issues": true
    },
    {
      "type": "pdf",
      "directory": "/path/to/architecture-docs/"
    }
  ]
}
```

Example 4 (markdown):
```markdown
# Analyze entire codebase
skill-seekers github --config configs/my-project-codebase.json
```

---

## Configuration Gallery | Skill Seekers

**URL:** https://skillseekersweb.com/configs

**Contents:**
- Config Gallery
- Featured
  - anthropic
  - catboost
  - chroma
  - cohere
  - angular
  - astro
  - django
  - express

178 ready-to-use configurations for Skill Seekers

Complete Anthropic API knowledge from official documentation. Use when building applications with Claude AI models. Covers Messages API, tool use, vision, streaming, extended thinking, batch API, and prompt engineering.

Complete CatBoost knowledge from official documentation. Use when building gradient boosting with native categorical feature support. Covers classification, regression, ranking, and GPU training.

Complete Chroma knowledge from official documentation. Use when building AI-native embeddings databases. Collections, embeddings, querying, filtering, multi-modal support, and client-server deployment.

Complete Cohere API knowledge from official documentation. Use when building applications with enterprise-grade LLMs. Covers generate, embed, classify, summarize, and rerank.

Complete Angular knowledge combining official documentation and source code. Use when building enterprise web applications with TypeScript. Covers components, services, routing, forms, and Angular CLI. Version 17+ with standalone components.

Complete Astro knowledge combining official documentation and Astro codebase. Use when building content-focused websites with islands architecture, partial hydration, and zero-JS by default. Covers v4.x with View Transitions.

Complete Django framework knowledge combining official documentation and Django codebase. Use when building Django applications, understanding ORM internals, or debugging Django issues.

Complete Express.js knowledge combining documentation and source code. Use when building Node.js web servers, APIs, or middleware. Covers routing, middleware, template engines, and production best practices.

Complete FastAPI knowledge combining official documentation and FastAPI codebase. Use when building FastAPI applications, understanding async patterns, or working with Pydantic models.

Complete Flask knowledge combining official documentation and source code. Use when building Python web applications, REST APIs, or microservices. Covers routing, templates, extensions, and deployment patterns.

Complete Hono framework knowledge combining official documentation and Hono codebase. Use when building Hono applications, understanding middleware, or debugging Hono issues.

Complete HTMX knowledge from official documentation. Use when building modern web applications with hypermedia, without JavaScript frameworks. Covers AJAX, CSS transitions, WebSockets, and SSE.

Use this skill when working with HTTPX, a fully featured HTTP client for Python 3 with sync and async APIs. HTTPX provides a familiar requests-like interface with support for HTTP/2, connection pooling, and comprehensive middleware capabilities.

Complete Laravel framework knowledge combining official documentation and Laravel codebase. Use when building Laravel applications, understanding Eloquent internals, or debugging Laravel issues.

Complete NestJS knowledge combining official documentation and source code. Use when building enterprise-grade Node.js applications with TypeScript. Covers modules, controllers, providers, dependency injection, and microservices.

Complete Next.js knowledge combining official documentation and Next.js source code. Use when building React applications with SSR, SSG, API routes, and App Router. Covers Next.js 14+ with App Router, Server Components, and edge runtime.

Complete Nuxt.js knowledge combining official documentation and source code. Use when building Vue-based universal applications with SSR, SSG, and file-based routing. Covers Nuxt 3 with Nitro engine and Vue 3 Composition API.

Complete TanStack Query (React Query) knowledge from official documentation. Use when managing server state in React applications. Covers queries, mutations, caching, optimistic updates, and infinite queries.

Complete React knowledge base combining official documentation and React codebase insights. Use when working with React, understanding API changes, or debugging React internals.

Complete Ruby on Rails knowledge combining official documentation and source code. Use when building full-stack web applications with Ruby. Covers MVC, Active Record, routing, and deployment.

Complete SolidJS knowledge from official documentation. Use when building high-performance reactive web applications without Virtual DOM. Covers signals, stores, effects, and routing.

Complete Svelte knowledge combining official documentation and source code. Use when building reactive web applications with compiled components. Covers Svelte 4 with runes, stores, animations, and transitions.

Complete SvelteKit knowledge combining documentation and source code. Use when building modern web apps with Svelte. Covers routing, server-side rendering, adapters, and full-stack Svelte development.

Complete Vue.js framework knowledge combining official documentation and Vue.js codebase. Use when building Vue applications, understanding reactivity internals, composition API, or debugging Vue issues.

Complete Zod knowledge from official documentation. Use when building type-safe schemas for TypeScript validation. Covers schema definition, parsing, inference, transformations, and error handling.

Complete Artillery knowledge from official documentation. Use when load testing APIs and applications. Covers scenarios, plugins, metrics, and distributed testing.

Complete Cypress knowledge from official documentation. Use when performing end-to-end testing for modern web applications. Covers commands, assertions, network handling, and CI/CD integration.

Complete Insomnia knowledge from official documentation. Use when designing, testing, and debugging APIs with an open-source client. Covers requests, collections, environments, and plugins.

Complete Jest knowledge from official documentation. Use when testing JavaScript applications with zero configuration. Covers matchers, async testing, mocks, snapshots, and coverage.

Complete k6 knowledge from official documentation. Use when load testing APIs and applications. Covers HTTP requests, scenarios, thresholds, extensions, and cloud execution.

Complete Playwright knowledge from official documentation. Use when testing modern web apps across multiple browsers. Covers locators, actions, auto-waiting, and parallel execution.

Complete Postman knowledge from official documentation. Use when building, testing, and documenting APIs. Covers collections, environments, tests, monitors, and Newman CLI.

Complete pytest knowledge from official documentation. Use when testing Python applications with simple syntax. Covers fixtures, markers, plugins, and parameterized testing.

Complete Selenium knowledge from official documentation. Use when automating browser testing across different platforms. Covers WebDriver, locators, waits, and grid.

Complete Testing Library knowledge from official documentation. Use when testing UI components with user-centric queries. Covers DOM Testing Library, React Testing Library, and best practices.

Complete Vitest knowledge from official documentation. Use when testing Vite-based projects with fast unit testing. Covers configuration, mocking, coverage, and in-source testing.

Complete Flutter knowledge from official documentation. Use when building cross-platform applications for mobile, web, and desktop with Dart. Covers widgets, state management, navigation, and platform integration.

Complete React Native knowledge from official documentation. Use when building cross-platform mobile applications with React. Covers components, navigation, native modules, and deployment to iOS/Android.

Complete Stripe knowledge from official documentation. Use when implementing payments, subscriptions, invoicing, or financial infrastructure. Covers Stripe.js, Payment Intents, Billing, and Connect.

Complete Elasticsearch knowledge from official documentation. Use when building search, analytics, or logging solutions. Covers indexing, querying, aggregations, and cluster management.

Complete Auth0 knowledge from official documentation. Use when implementing authentication and authorization in applications. Covers universal login, APIs, rules, actions, and organizations.

Complete Clerk knowledge from official documentation. Use when adding authentication and user management to React/Next.js applications. Covers sign-in, sessions, organizations, and webhooks.

Complete Sentry knowledge from official documentation. Use when monitoring application errors and performance. Covers error tracking, performance monitoring, release health, and distributed tracing.

Complete Apache Kafka knowledge from official documentation. Use when building event-driven architectures and real-time data pipelines. Covers producers, consumers, topics, partitions, and Kafka Streams.

Complete RabbitMQ knowledge from official documentation. Use when building distributed systems with message queuing. Covers exchanges, queues, bindings, routing, and clustering.

Complete TypeScript knowledge from official documentation. Use when building type-safe JavaScript applications. Covers types, interfaces, generics, decorators, modules, and compiler options.

Complete D3.js knowledge from official documentation. Use when creating data visualizations with custom SVG, Canvas, and HTML. Covers selections, scales, axes, transitions, and geographic projections.

Complete Three.js knowledge from official documentation. Use when building 3D graphics in the browser with WebGL. Covers scenes, cameras, materials, lighting, geometries, and animation.

Complete Steam Economy system knowledge from official documentation. Use for ISteamInventory API, ISteamEconomy API, IInventoryService Web API, Steam Wallet integration, in-app purchases, item definitions, trading, crafting, market integration, and all economy features for game developers.

Complete Adventure Game Studio knowledge from official documentation. Use when building point-and-click adventure games. Covers rooms, characters, inventory, dialogue, and scripting with AGS Script.

Complete AppGameKit knowledge from official documentation. Use when building cross-platform games with BASIC-like scripting. Covers 2D/3D graphics, physics, multiplayer, and VR.

Complete Armory3D knowledge from official documentation. Use when building 3D games integrated with Blender. Covers nodes-based logic, Haxe scripting, rendering, and physics.

Complete Babylon.js knowledge from official documentation. Use when building 3D web applications and games with WebGL/WebGPU. Covers meshes, materials, physics, particles, and GUI systems.

Complete Bevy knowledge from official documentation. Use when building data-driven games in Rust with ECS architecture. Covers systems, components, resources, queries, and rendering.

Complete Bitsy knowledge from official documentation and community resources. Use when creating tiny narrative games in the browser. Covers rooms, sprites, items, dialogue, and game variables.

Complete Clickteam Fusion knowledge from official documentation. Use when building 2D games without coding using event-based visual programming. Covers frame editor, objects, events, and exporters.

Complete Cocos2d-x knowledge from official documentation. Use when building cross-platform 2D games in C++, Lua, or JavaScript. Covers scenes, sprites, actions, physics, and particle systems.

Complete Construct 3 knowledge from official documentation. Use when building HTML5 games without coding using visual scripting. Covers events, behaviors, effects, and multiplayer.

Complete Defold knowledge from official documentation. Use when building 2D games with a data-driven approach. Covers game objects, components, Lua scripting, particle effects, and physics.

Complete Flax Engine knowledge from official documentation. Use when building modern 3D games with C++ or C#. Covers visual scripting, physics, rendering, and editor extensibility.

Complete GameMaker knowledge from official documentation. Use when building 2D games with drag-and-drop or GML scripting. Covers objects, rooms, sprites, physics, and multiplayer.

Complete GDevelop knowledge from official documentation. Use when building games without coding using visual events. Covers behaviors, effects, physics, and export to multiple platforms.

Complete Godot Engine knowledge combining official documentation and source code. Use when building 2D/3D games, tools, or interactive experiences with Godot 4. Covers GDScript, nodes, physics, signals, rendering, and the Godot API.

Complete HaxeFlixel knowledge from official documentation. Use when building 2D games in Haxe with cross-platform support. Covers sprites, tilemaps, camera, UI, and effects.

Complete Heaps.io knowledge from official documentation. Use when building high-performance 2D/3D games in Haxe. Covers graphics, shaders, ECS, and resource management.

Complete LÖVE (Love2D) knowledge from official documentation. Use when building 2D games in Lua. Covers graphics, audio, physics, input, and file I/O.

Complete MonoGame knowledge from official documentation. Use when building cross-platform games with C# and XNA compatibility. Covers graphics, audio, input, content pipeline, and shaders.

Complete Open 3D Engine (O3DE) knowledge from official documentation. Use when building AAA-quality 3D games and simulations. Covers Atom renderer, Script Canvas, physics, and multiplayer networking.

Complete Panda3D knowledge from official documentation. Use when building 3D games and simulations in Python or C++. Covers scene graph, physics, rendering, and pipeline tools.

Complete Phaser 3 knowledge from official documentation. Use when building HTML5 games for web and mobile. Covers scenes, sprites, physics, tilemaps, and WebGL rendering.

Complete PICO-8 knowledge from official documentation. Use when creating retro-style games with Lua in a fantasy console environment. Covers graphics, sound, music, and cartridge sharing.

Complete PlayCanvas knowledge from official documentation. Use when building WebGL and WebGPU games that run in browsers. Covers entity system, rendering, physics, and cloud-based development.

Complete Pygame knowledge from official documentation. Use when building 2D games in Python. Covers display, surfaces, sprites, collision detection, and sound.

Complete Raylib knowledge from official documentation. Use when learning game programming with a simple C library. Covers graphics, audio, input, physics, and shaders.

Complete Ren'Py knowledge from official documentation. Use when building visual novels and story-based games. Covers scripting, characters, images, audio, and GUI customization.

Complete RPG Maker knowledge from official documentation. Use when building JRPG-style games without programming. Covers maps, events, database, and scripting with Ruby/JavaScript.

Complete Solar2D knowledge from official documentation. Use when building 2D mobile games and apps with Lua. Covers Corona Simulator, graphics, physics, widgets, and native plugins.

Complete Stencyl knowledge from official documentation. Use when building 2D games with visual block-based programming. Covers actor types, scenes, behaviors, and publishing to multiple platforms.

Complete Stride knowledge from official documentation. Use when building cross-platform 3D games with C# and .NET. Covers ECS, rendering, physics, animation, and scripting.

Complete Torque3D knowledge from official documentation. Use when building open-source 3D games with C++ and TorqueScript. Covers terrain, vehicles, multiplayer, and world editor.

Complete Twine knowledge from official documentation. Use when building interactive fiction and branching narratives. Covers story formats, variables, macros, styling with CSS, and JavaScript.

Complete Unity knowledge from official documentation. Use when building 2D/3D games, VR/AR applications, and interactive experiences. Covers C# scripting, physics, rendering, animation, and multiplayer networking.

Complete Unreal Engine 5 knowledge from official documentation. Use when building high-fidelity 3D games, architectural visualizations, and virtual productions. Covers Blueprints, C++, Niagara, Lumen, and MetaHuman.

Complete Urho3D knowledge from official documentation. Use when building lightweight 3D games with C++, AngelScript, or Lua. Covers scene management, rendering, physics, and scripting.

Complete Ansible automation knowledge combining official documentation and Ansible Core codebase. Use when writing playbooks, roles, and modules for automating infrastructure management, configuration management, and application deployment.

Complete Docker knowledge combining official documentation and Moby source code. Use when containerizing applications, writing Dockerfiles, managing containers, or orchestrating with Docker Compose. Covers Docker Engine, CLI, BuildKit, and best practices.

Complete GitHub Actions knowledge from official documentation. Use when creating CI/CD pipelines, automating workflows, or building GitHub integrations. Covers workflow syntax, reusable workflows, actions, runners, and deployment environments.

Complete Grafana knowledge from official documentation. Use when visualizing metrics, logs, traces, and creating dashboards. Covers data sources, panels, alerting, Grafana Cloud, and the Grafana plugin ecosystem.

Complete Helm knowledge from official documentation. Use when packaging Kubernetes applications, managing charts, or templating deployments. Covers Helm 3, chart development, OCI registries, and Helmfile.

Complete Kubernetes orchestration knowledge combining official documentation and Kubernetes codebase. Use when deploying, managing, or debugging Kubernetes clusters and workloads.

Complete Prometheus knowledge from official documentation. Use when monitoring systems and applications with time-series metrics. Covers PromQL querying, scraping, alerting, exporters, and Alertmanager.

Complete Terraform knowledge combining documentation and source code. Use when writing infrastructure as code, managing cloud resources, or implementing GitOps workflows. Covers HCL, providers, modules, and state management.

Complete HashiCorp Vault knowledge from official documentation. Use when managing secrets, encryption, and identity-based access. Covers secrets engines, authentication methods, policies, PKI, and dynamic credentials.

Complete Claude Code CLI knowledge combining official documentation and source code. Use for Claude Code features, tools, MCP integration, hooks, settings, IDE integrations, agent workflows, and AI-assisted development.

Complete Docker Compose knowledge from official documentation. Use when defining and running multi-container Docker applications. Covers services, networks, volumes, profiles, secrets, health checks, and the Compose Specification.

Complete ESLint knowledge from official documentation. Use when configuring JavaScript and TypeScript linting. Covers flat config (ESLint 9+), rules, plugins, custom rules, TypeScript integration, and editor integrations.

Complete Git knowledge from official documentation and Pro Git book. Use when version controlling source code. Covers branching, merging, rebasing, remotes, hooks, submodules, and worktrees.

Complete Prettier knowledge from official documentation. Use when formatting code consistently across projects. Covers configuration, plugins, editor integrations, linter integration, and all supported languages.

Complete Storybook 8 knowledge from official documentation. Use when building UI component libraries and design systems. Covers stories, addons, component testing, accessibility, theming, and documentation.

Complete Visual Studio Code knowledge from official documentation. Use when editing, debugging, and developing code. Covers extensions, debugging, tasks, settings, remote development, Copilot AI features, and the extension API.

Complete Zod knowledge from official documentation. Use when building type-safe TypeScript applications with runtime validation. Covers schemas, parsing, transformations, error handling, and Zod v4 features.

Complete Apache Cassandra knowledge from official documentation. Use when building highly scalable, distributed NoSQL databases. Covers CQL, data modeling, replication, storage engine, and performance tuning.

Complete CockroachDB knowledge from official documentation. Use when building distributed, horizontally scalable SQL databases. Covers SQL, distributed transactions, multi-region deployment, replication, and changefeeds.

Complete Drizzle ORM knowledge from official documentation. Use when building type-safe database applications with SQL-like syntax in TypeScript. Covers schema definition, queries, relations, transactions, migrations, and multi-database support.

Complete Amazon DynamoDB knowledge from official documentation. Use when building serverless, NoSQL applications at any scale. Covers data modeling, PartiQL, streams, DAX, global tables, and transactions.

Complete Fauna knowledge from official documentation. Use when working with Fauna's document-relational database. Covers FQL v10, collections, indexes, access control, and ACID transactions. Note: Fauna's serverless cloud service was discontinued in September 2024; this config is maintained for legacy projects.

Complete MariaDB knowledge from official documentation. Use when building applications with the open-source MySQL-compatible database. Covers SQL, storage engines, Galera Cluster, replication, window functions, and JSON support.

Complete MongoDB knowledge combining documentation and source code. Use when designing NoSQL databases, writing aggregation pipelines, or managing document-based data. Covers CRUD, aggregation, indexes, Atlas, transactions, change streams, and vector search.

Complete MySQL 8.4 LTS knowledge from official documentation. Use when building applications with the world's most popular open-source relational database. Covers SQL, replication, partitioning, performance tuning, and JSON support.

Complete Neo4j knowledge from official documentation. Use when building graph database applications. Covers Cypher query language, graph modeling, APOC, Graph Data Science library, and Neo4j Aura cloud.

Complete Oracle Database knowledge from official documentation. Use when building enterprise applications with the world's leading relational database. Covers SQL, PL/SQL, partitioning, RAC, Data Guard, and performance tuning.

Complete PostgreSQL knowledge combining official documentation and source code. Use when designing databases, writing queries, optimizing performance, or managing PostgreSQL instances. Covers SQL, administration, extensions, and advanced features.

Complete Prisma knowledge from official documentation. Use when building type-safe database applications with Node.js and TypeScript. Covers Prisma ORM schema definition, client queries, migrations, relations, and Prisma Accelerate.

Complete Redis knowledge combining documentation and source code. Use when implementing caching, message queues, real-time features, session storage, or vector search. Covers data structures, persistence, clustering, Redis Stack, and vector search.

Complete SQLite knowledge from official documentation. Use when building embedded, serverless databases for applications. Covers SQL, full-text search (FTS5), R*Trees, JSON functions, WAL mode, and the C API.

Complete Supabase knowledge from official documentation. Use when building applications with the open-source Firebase alternative. Covers PostgreSQL, Auth, Real-time, Edge Functions, Storage, and AI/vector search with pgvector.

Complete TimescaleDB knowledge from official documentation. Use when building time-series applications on PostgreSQL. Covers hypertables, continuous aggregates, compression, data retention, tiered storage, and user-defined actions.

Complete NumPy knowledge from official documentation. Use when performing numerical computing, array operations, or mathematical computations in Python. Covers ndarrays, broadcasting, linear algebra, FFT, and random sampling.

Complete Pandas knowledge combining documentation and source code. Use when manipulating tabular data, cleaning datasets, or performing data analysis in Python. Covers DataFrames, Series, indexing, groupby, time series, and styling.

Complete PyTorch knowledge from official documentation. Use when building deep learning models, neural networks, or performing GPU-accelerated computations. Covers tensors, autograd, nn modules, torch.compile, FSDP distributed training, and deployment.

Complete TensorFlow 2.x knowledge from official documentation. Use when building production ML models, deep learning applications, or deploying AI solutions. Covers Keras, tf.data, tf.function, TFLite, TF.js, and TensorBoard.

Complete Bulma knowledge from official documentation. Use when building responsive web interfaces with a modern CSS-only framework. Covers the grid system, layout, elements, components, form controls, helpers, and Bulma v1 CSS variables with dark mode support.

Complete Chakra UI v3 knowledge from official documentation. Use when building accessible React applications with composable, themeable components. Covers the new recipe-based theming system, styling props, component library, and composition patterns.

Complete Foundation for Sites knowledge from official documentation. Use when building responsive, accessible websites with this enterprise-grade CSS framework. Covers the XY grid, typography, components, forms, JavaScript plugins, and Sass customization.

Complete MUI Material UI knowledge from official documentation. Use when building React applications with Material Design components. Covers all components, theming, the sx prop, system utilities, icons, and the Data Grid.

Complete shadcn/ui knowledge from official documentation. Use when building accessible React components with Radix UI primitives and Tailwind CSS. Covers components, theming, dark mode, CLI usage, and framework-specific installation guides.

Complete Tailwind CSS knowledge combining official documentation and Tailwind codebase. Use when styling with Tailwind utility classes or customizing configuration. Covers v4 CSS-first configuration with @theme and @utility directives, responsive design, dark mode, plugins, and all utility classes.

Complete Contentful knowledge from official documentation. Use when building headless CMS applications with content delivery APIs. Covers content modeling, SDKs, GraphQL, webhooks, environments, and the App Framework.

Complete Docusaurus knowledge from official documentation. Use when building documentation websites with Markdown, MDX, and React. Covers configuration, theming, plugins, versioning, i18n, search, and deployment.

Complete Strapi knowledge from official documentation. Use when building headless CMS APIs with a customizable admin panel. Covers content types, REST and GraphQL APIs, authentication, plugins, TypeScript, and deployment.

Complete AWS Boto3 knowledge from official documentation. Use when building Python applications that interact with AWS services. Covers S3, EC2, Lambda, DynamoDB, SQS, SNS, IAM, CloudWatch, and 200+ AWS services.

Complete Microsoft Azure knowledge from official documentation. Use when building applications on Microsoft's cloud platform. Covers compute, storage, databases, networking, identity, AI/ML, and DevOps services.

Complete Cloudflare knowledge from official documentation. Use when securing, accelerating, and building on the edge. Covers CDN, DNS, Workers, Pages, R2, D1, Queues, Workers AI, and Zero Trust.

Complete DigitalOcean knowledge from official documentation. Use when deploying applications on the developer cloud. Covers Droplets, Kubernetes, App Platform, managed databases, Spaces, networking, and the doctl CLI.

Complete Firebase knowledge from official documentation. Use when building mobile and web applications with Google's backend platform. Covers Firestore, Realtime Database, Auth, Cloud Functions, Hosting, Storage, Cloud Messaging, and Analytics.

Complete Google Cloud Platform knowledge from official documentation. Use when building applications on GCP. Covers Compute Engine, Cloud Run, GKE, Cloud Storage, BigQuery, Cloud SQL, Pub/Sub, IAM, and Cloud Build.

Complete Heroku knowledge from official documentation. Use when deploying, managing, and scaling applications on the platform-as-a-service. Covers dynos, add-ons, Postgres, pipelines, review apps, config vars, and the Heroku CLI.

Complete Netlify knowledge from official documentation. Use when deploying web applications with CI/CD, serverless functions, edge functions, and global CDN. Covers builds, deploys, functions, forms, identity, blob storage, and CLI.

Complete Vercel knowledge from official documentation. Use when deploying frontend applications and serverless functions with global edge infrastructure. Covers deployments, serverless functions, edge functions, preview environments, storage, and CLI.

Complete esbuild knowledge from official documentation. Use when bundling JavaScript with extremely fast build speeds. Covers API, plugins, loaders, and transformations.

Complete Rollup knowledge from official documentation. Use when bundling JavaScript libraries with ES modules. Covers configuration, plugins, tree-shaking, and output formats.

Complete Storybook knowledge from official documentation. Use when developing UI components in isolation. Covers configuration, addons, testing, and documentation.

Complete SWC knowledge from official documentation. Use when transforming JavaScript and TypeScript with Rust-based speed. Covers compilation, minification, and bundling.

Complete Turborepo knowledge from official documentation. Use when building monorepos with efficient task running and caching. Covers configuration, pipelines, caching, remote caching, and filtering.

Complete Vite knowledge from official documentation. Use when building modern web applications with fast HMR and optimized builds. Covers configuration, plugins, SSR, and library mode.

Complete Webpack knowledge from official documentation. Use when bundling JavaScript applications with custom configurations. Covers entry/output, loaders, plugins, optimization, and development server.

Complete GraphQL knowledge from official documentation. Use when designing APIs, querying data, or implementing type-safe data fetching. Covers schema, queries, mutations, subscriptions, variables, directives, introspection, and best practices.

Complete tRPC v11 knowledge from official documentation. Use when building end-to-end type-safe APIs with TypeScript. Covers routers, procedures, middleware, context, subscriptions, TanStack Query integration, server adapters, and error handling.

Complete Anthropic API knowledge from official documentation. Use when building applications with Claude AI models. Covers Messages API, tool use, vision, streaming, extended thinking, batch API, and prompt engineering.

Complete CatBoost knowledge from official documentation. Use when building gradient boosting with native categorical feature support. Covers classification, regression, ranking, and GPU training.

Complete Chroma knowledge from official documentation. Use when building AI-native embeddings databases. Collections, embeddings, querying, filtering, multi-modal support, and client-server deployment.

Complete Cohere API knowledge from official documentation. Use when building applications with enterprise-grade LLMs. Covers generate, embed, classify, summarize, and rerank.

Complete DeepSpeed knowledge from official documentation. Use when training large-scale deep learning models with optimization. Covers ZeRO, mixed precision, pipeline parallelism, and inference.

Complete DVC (Data Version Control) knowledge from official documentation. Use when versioning data, models, and ML pipelines. Covers data versioning, pipelines, experiments, and storage.

Complete fast.ai knowledge from official documentation. Use when building practical deep learning applications quickly. Covers vision, text, tabular, and collaborative filtering.

Complete Gensim knowledge from official documentation. Use when training and using word embeddings and topic models. Covers Word2Vec, Doc2Vec, LDA, and similarity queries.

Complete Hugging Face knowledge from official documentation. Use when working with transformer models, datasets, and ML pipelines. Covers Transformers, Datasets, Tokenizers, Accelerate, and model hub.

Complete JAX knowledge from official documentation. Use when building high-performance ML research code with automatic differentiation. Covers NumPy, transformations, JIT, grad, vmap, and pmap.

Complete Keras 3 knowledge from official documentation. Use when building deep learning models with a user-friendly API. Covers models, layers, training, callbacks, and multi-backend support.

Complete Kubeflow knowledge from official documentation. Use when deploying ML workflows on Kubernetes. Covers notebooks, pipelines, training, serving, and hyperparameter tuning.

Complete LangChain knowledge from official documentation. Use when building LLM-powered applications with chains, agents, and RAG. Covers LangChain Python v0.3+, LCEL, LangGraph, LangSmith, and integrations with major LLM providers.

Complete LightGBM knowledge from official documentation. Use when building fast, distributed gradient boosting models. Covers histogram-based learning, GOSS, EFB, and categorical features.

Complete LlamaIndex knowledge from official documentation. Use when building RAG applications and data frameworks for LLMs. Covers indexing, querying, agents, and multi-modal.

Complete Matplotlib knowledge from official documentation. Use when creating static, animated, and interactive visualizations in Python. Covers pyplot, artists, backends, and customization.

Complete MLflow knowledge from official documentation. Use when managing ML lifecycle including experiments, models, and deployments. Covers tracking, projects, models, and registry.

Complete Modin knowledge from official documentation. Use when scaling pandas workflows with distributed computing. Covers DataFrame API, backends, and parallel execution.

Complete NLTK knowledge from official documentation. Use when building NLP applications with classic algorithms. Covers tokenization, parsing, classification, and corpora.

Complete Ollama knowledge from official documentation. Use when running LLMs locally. Covers model pulling, chatting, custom models, Modelfile, REST API, OpenAI-compatible API, and GPU setup.

Complete ONNX knowledge from official documentation. Use when deploying ML models across frameworks. Covers model conversion, runtime, operators, and optimization.

Complete OpenAI API knowledge from official documentation. Use when integrating GPT-4o, o1, o3, DALL-E, Whisper, or embedding models into applications. Covers Responses API, function calling, structured outputs, fine-tuning, realtime, and best practices.

Complete OpenCV knowledge from official documentation. Use when building computer vision applications. Covers image processing, feature detection, object detection, video analysis, and deep learning.

Complete Pinecone knowledge from official documentation. Use when building vector search applications at scale. Covers indexes, vectors, metadata filtering, hybrid search, and namespaces.

Complete Plotly knowledge from official documentation. Use when creating interactive web-based visualizations. Covers Plotly Express, Graph Objects, Dash, and animation.

Complete PyTorch Lightning knowledge from official documentation. Use when structuring PyTorch code with best practices. Covers LightningModule, Trainer, callbacks, and distributed training.

Complete Ray knowledge from official documentation. Use when building distributed Python applications and scaling ML workloads. Covers tasks, actors, train, tune, serve, and data.

Complete scikit-learn knowledge from official documentation. Use when implementing classical machine learning algorithms. Covers classification, regression, clustering, dimensionality reduction, and model selection.

Complete Seaborn knowledge from official documentation. Use when creating statistical visualizations with beautiful defaults. Covers relational, distributional, and categorical plots.

Complete spaCy knowledge from official documentation. Use when building production-grade NLP pipelines. Covers tokenization, tagging, parsing, NER, transformers, and custom components.

Complete vLLM knowledge from official documentation. Use when serving LLMs with high throughput and low latency. Covers PagedAttention, continuous batching, tensor parallelism, and OpenAI-compatible API.

Complete Weights & Biases knowledge from official documentation. Use when tracking experiments, visualizing results, and managing ML models. Covers runs, sweeps, artifacts, and reports.

Complete Weaviate knowledge from official documentation. Use when building vector search with GraphQL interface. Covers schema, modules, hybrid search, and multi-tenant architecture.

Complete XGBoost knowledge from official documentation. Use when building gradient boosting models for structured data. Covers classification, regression, ranking, and distributed training.

Created a config for a framework not listed here? Share it with the community!

Paste your unified config JSON below to validate it before submitting. Supports documentation, GitHub, and PDF sources.

Need a starting point?

Load an example config or browse 27+ presets from the gallery

💡 Tip: Browse the config gallery above to see 27+ real examples

We review submissions within 24-48 hours

All configs are tested before adding

Your GitHub profile listed as contributor

---
