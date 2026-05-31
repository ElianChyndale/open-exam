import{i as e}from"./preload-helper-D2yxXLVK.js";import{b as t}from"./iframe-OLn_dhfG.js";import{a as n,c as r,d as i,f as a,i as o,l as s,n as c,o as l,p as u,r as d,s as f,t as p,u as m}from"./ui-wgBh5Z1T.js";var h,g,_,v,y,b;e((()=>{h=t(),u(),g={title:`Foundation/Apple Workspace Kit`,component:i,parameters:{layout:`centered`}},_={render:()=>(0,h.jsxs)(i,{className:`w-[min(760px,90vw)] space-y-5`,children:[(0,h.jsxs)(`div`,{children:[(0,h.jsx)(`p`,{className:`metric-label`,children:`OpenExam UI Foundation`}),(0,h.jsx)(`h1`,{className:`mt-1 text-2xl font-semibold tracking-tight`,children:`Apple workspace primitives`})]}),(0,h.jsxs)(`div`,{className:`flex flex-wrap gap-2`,children:[(0,h.jsx)(d,{children:`Start review`}),(0,h.jsx)(d,{variant:`secondary`,children:`Open map`}),(0,h.jsx)(d,{variant:`ghost`,children:`Dismiss`}),(0,h.jsx)(d,{variant:`danger`,children:`Skip task`})]}),(0,h.jsxs)(`div`,{className:`flex flex-wrap gap-2`,children:[(0,h.jsx)(c,{tone:`accent`,children:`Official registry`}),(0,h.jsx)(c,{tone:`success`,children:`Completed`}),(0,h.jsx)(c,{tone:`warning`,children:`Due today`}),(0,h.jsx)(c,{tone:`danger`,children:`High risk`})]}),(0,h.jsxs)(`div`,{className:`grid gap-3 md:grid-cols-3`,children:[(0,h.jsx)(f,{label:`Due reviews`,value:`12`,detail:`4 high-confidence errors`}),(0,h.jsx)(f,{label:`Study window`,value:`90 min`,detail:`Peak energy`}),(0,h.jsx)(f,{label:`Weak LOS`,value:`3`,detail:`Needs retrieval`})]}),(0,h.jsx)(p,{children:`Run a short retrieval drill before opening the answer.`}),(0,h.jsxs)(`div`,{className:`grid gap-3 md:grid-cols-2`,children:[(0,h.jsx)(n,{"aria-label":`Exam date`,type:`date`}),(0,h.jsx)(s,{"aria-label":`Study phase`,defaultValue:`review`,children:(0,h.jsx)(`option`,{value:`review`,children:`Review phase`})}),(0,h.jsx)(a,{"aria-label":`Reflection`,placeholder:`What changed your decision?`}),(0,h.jsx)(r,{"aria-label":`Search knowledge`,placeholder:`Search modules, formulas, traps...`})]}),(0,h.jsx)(l,{children:`LOS review rows stay quiet until they need attention.`}),(0,h.jsx)(m,{title:`Empty state`,children:(0,h.jsx)(o,{title:`Nothing due yet`,detail:`New cards appear after a mistake is captured.`})})]})},v={..._,decorators:[e=>(0,h.jsx)(`div`,{className:`theme-dark bg-surface-canvas p-8 text-ink`,children:(0,h.jsx)(e,{})})]},y={..._,parameters:{viewport:{defaultViewport:`mobile1`}}},_.parameters={..._.parameters,docs:{..._.parameters?.docs,source:{originalSource:`{
  render: () => <Surface className="w-[min(760px,90vw)] space-y-5">\r
      <div>\r
        <p className="metric-label">OpenExam UI Foundation</p>\r
        <h1 className="mt-1 text-2xl font-semibold tracking-tight">Apple workspace primitives</h1>\r
      </div>\r
      <div className="flex flex-wrap gap-2">\r
        <Button>Start review</Button>\r
        <Button variant="secondary">Open map</Button>\r
        <Button variant="ghost">Dismiss</Button>\r
        <Button variant="danger">Skip task</Button>\r
      </div>\r
      <div className="flex flex-wrap gap-2">\r
        <Badge tone="accent">Official registry</Badge>\r
        <Badge tone="success">Completed</Badge>\r
        <Badge tone="warning">Due today</Badge>\r
        <Badge tone="danger">High risk</Badge>\r
      </div>\r
      <div className="grid gap-3 md:grid-cols-3">\r
        <Metric label="Due reviews" value="12" detail="4 high-confidence errors" />\r
        <Metric label="Study window" value="90 min" detail="Peak energy" />\r
        <Metric label="Weak LOS" value="3" detail="Needs retrieval" />\r
      </div>\r
      <Alert>Run a short retrieval drill before opening the answer.</Alert>\r
      <div className="grid gap-3 md:grid-cols-2">\r
        <Field aria-label="Exam date" type="date" />\r
        <Select aria-label="Study phase" defaultValue="review"><option value="review">Review phase</option></Select>\r
        <TextArea aria-label="Reflection" placeholder="What changed your decision?" />\r
        <SearchField aria-label="Search knowledge" placeholder="Search modules, formulas, traps..." />\r
      </div>\r
      <ListRow>LOS review rows stay quiet until they need attention.</ListRow>\r
      <Sheet title="Empty state"><EmptyState title="Nothing due yet" detail="New cards appear after a mistake is captured." /></Sheet>\r
    </Surface>
}`,..._.parameters?.docs?.source}}},v.parameters={...v.parameters,docs:{...v.parameters?.docs,source:{originalSource:`{
  ...PrimitiveGallery,
  decorators: [Story => <div className="theme-dark bg-surface-canvas p-8 text-ink"><Story /></div>]
}`,...v.parameters?.docs?.source}}},y.parameters={...y.parameters,docs:{...y.parameters?.docs,source:{originalSource:`{
  ...PrimitiveGallery,
  parameters: {
    viewport: {
      defaultViewport: 'mobile1'
    }
  }
}`,...y.parameters?.docs?.source}}},b=[`PrimitiveGallery`,`PrimitiveGalleryDark`,`PrimitiveGalleryMobile`]}))();export{_ as PrimitiveGallery,v as PrimitiveGalleryDark,y as PrimitiveGalleryMobile,b as __namedExportsOrder,g as default};