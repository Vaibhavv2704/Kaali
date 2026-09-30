import * as React from 'react';
import {Slot} from '@radix-ui/react-slot';
import * as Dialog from '@radix-ui/react-dialog';
import * as TabsPrimitive from '@radix-ui/react-tabs';
import {cva,type VariantProps} from 'class-variance-authority';
import {motion,useReducedMotion} from 'framer-motion';
import {X} from 'lucide-react';
import {cn} from '../../lib/utils';
// Shadcn-style, locally owned primitives composed on Radix for keyboard/focus semantics.
const buttonVariants=cva('ui-button',{variants:{variant:{default:'button-default',secondary:'button-secondary',ghost:'button-ghost',help:'button-help',risk:'button-risk'},size:{default:'',icon:'button-icon',small:'button-small'}},defaultVariants:{variant:'default',size:'default'}});
export const Button=React.forwardRef<HTMLButtonElement,React.ButtonHTMLAttributes<HTMLButtonElement>&VariantProps<typeof buttonVariants>&{asChild?:boolean}>(({className,variant,size,asChild=false,...props},ref)=>{const Comp=asChild?Slot:'button';return <Comp ref={ref} className={cn(buttonVariants({variant,size}),className)} {...props}/>});Button.displayName='Button';
export function Glass({className,...props}:React.HTMLAttributes<HTMLDivElement>){return <div className={cn('glass',className)} {...props}/>}
export function Card({className,...props}:React.HTMLAttributes<HTMLDivElement>){return <Glass className={cn('bento-card',className)} {...props}/>}
export function Chip({active,className,...props}:React.ButtonHTMLAttributes<HTMLButtonElement>&{active?:boolean}){return <button aria-pressed={active} className={cn('chip',active&&'chip-active',className)} {...props}/>}
export const Tabs=TabsPrimitive.Root;
export const TabsList=React.forwardRef<React.ElementRef<typeof TabsPrimitive.List>,React.ComponentPropsWithoutRef<typeof TabsPrimitive.List>>(({className,...props},ref)=><TabsPrimitive.List ref={ref} className={cn('tabs-list',className)} {...props}/>);TabsList.displayName='TabsList';
export const TabsTrigger=React.forwardRef<React.ElementRef<typeof TabsPrimitive.Trigger>,React.ComponentPropsWithoutRef<typeof TabsPrimitive.Trigger>>(({className,...props},ref)=><TabsPrimitive.Trigger ref={ref} className={cn('tabs-trigger',className)} {...props}/>);TabsTrigger.displayName='TabsTrigger';
export const TabsContent=TabsPrimitive.Content;
export function Sheet({open,onOpenChange,title,children,closeLabel="Close",description}:{open:boolean;onOpenChange:(open:boolean)=>void;title:string;children:React.ReactNode;closeLabel?:string;description?:string}){const reduce=useReducedMotion();return <Dialog.Root open={open} onOpenChange={onOpenChange}><Dialog.Portal><Dialog.Overlay className="sheet-overlay"/><Dialog.Content className="glass sheet"><motion.div initial={reduce?false:{y:20,opacity:0}} animate={{y:0,opacity:1}} transition={{type:'spring',stiffness:280,damping:28}}><Dialog.Title>{title}</Dialog.Title><Dialog.Description className="sr-only">{description??`${title}. Choose an option below.`}</Dialog.Description><Dialog.Close asChild><Button variant="ghost" size="icon" className="sheet-close" aria-label={closeLabel}><X size={20}/></Button></Dialog.Close>{children}</motion.div></Dialog.Content></Dialog.Portal></Dialog.Root>}
export function Skeleton(){return <div className="skeleton" role="status" aria-label="Loading"><span className="sr-only">Loading…</span></div>}
export function Toast({children,onClose}:{children:React.ReactNode;onClose:()=>void}){return <Glass className="toast" role="status"><span>{children}</span><Button size="icon" variant="ghost" aria-label="Dismiss message" onClick={onClose}><X size={16}/></Button></Glass>}
